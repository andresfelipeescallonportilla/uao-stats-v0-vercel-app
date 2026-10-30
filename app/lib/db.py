#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Shared PostgreSQL engine for every dashboard module.

Connection settings are resolved from environment variables, in this order:
  1. DATABASE_URL                       (e.g. Supabase pooler connection string)
  2. DB_HOST / DB_PORT / DB_USER / DB_PASSWORD / DB_NAME
  3. POSTGRES_URL_NON_POOLING / POSTGRES_URL (injected by the Vercel Supabase integration)

Local development keeps working with DB_HOST=localhost (no SSL is forced for local hosts).
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.engine import URL, make_url
from sqlalchemy.pool import NullPool

LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1"}
SUPPORTED_QUERY_PARAMS = {"sslmode", "sslrootcert", "connect_timeout", "application_name", "options"}


def _from_parts():
    host = os.environ.get("DB_HOST")
    if not host:
        return None
    return URL.create(
        "postgresql+psycopg",
        username=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", ""),
        host=host,
        port=int(os.environ.get("DB_PORT", "5432")),
        database=os.environ.get("DB_NAME", "postgres"),
    )


def _from_url(raw):
    if raw.startswith("postgres://"):
        raw = "postgresql://" + raw[len("postgres://"):]
    url = make_url(raw).set(drivername="postgresql+psycopg")
    # Vercel/Supabase URLs can carry params like `supa=` that libpq rejects.
    query = {k: v for k, v in url.query.items() if k in SUPPORTED_QUERY_PARAMS}
    return url.set(query=query)


def _resolve_url():
    if os.environ.get("DATABASE_URL"):
        return _from_url(os.environ["DATABASE_URL"])
    parts = _from_parts()
    if parts is not None:
        return parts
    for key in ("POSTGRES_URL_NON_POOLING", "POSTGRES_URL"):
        if os.environ.get(key):
            return _from_url(os.environ[key])
    raise RuntimeError(
        "Database is not configured. Set DATABASE_URL or DB_HOST/DB_PORT/DB_USER/DB_PASSWORD/DB_NAME."
    )


def get_engine():
    url = _resolve_url()
    if url.host not in LOCAL_HOSTS and "sslmode" not in url.query:
        url = url.update_query_dict({"sslmode": "require"})

    serverless = bool(os.environ.get("VERCEL"))
    return create_engine(
        url,
        # Serverless instances are short-lived; let the Supabase pooler own pooling there.
        poolclass=NullPool if serverless else None,
        pool_pre_ping=not serverless,
        # Server-side prepared statements break on Supabase's transaction pooler (port 6543).
        connect_args={"prepare_threshold": None, "connect_timeout": 10},
    )


connDB = get_engine()
