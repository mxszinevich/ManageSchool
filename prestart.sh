#! /usr/bin/env bash

sleep 5;
celery -A config worker -l info --concurrency=8 -n worker1@%n
sleep 10;
celery -A config worker -l info --concurrency=8 -n worker2@%n