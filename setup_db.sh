#!/bin/bash

sqlite3 "password_manager.db" ".read schema.sql"
