#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────
# BusinessCore — Start All Platform APIs
# ──────────────────────────────────────────────────────────────
set -e

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
LOGS="$BASE_DIR/logs"
mkdir -p "$LOGS"

PORTS=(8000 8001 8002 8003 8004 8005 8006 8007 8008 8009 8010 8011)
APPS=(
  "modules.party.infrastructure.api.party_api"
  "modules.item.infrastructure.api.item_api"
  "modules.organization.infrastructure.api.org_api"
  "modules.catalog.infrastructure.api.catalog_api"
  "modules.warehouse.infrastructure.api.warehouse_api"
  "modules.inventory.infrastructure.api.inventory_api"
  "modules.workflow.infrastructure.api.workflow_api"
  "modules.document.infrastructure.api.document_api"
  "modules.sales.core.infrastructure.api.sales_api"
  "modules.purchase.core.infrastructure.api.purchase_api_main"
  "modules.notification.infrastructure.api.notification_api"
  "modules.procurement.core.infrastructure.api.procurement_api_main"
)
NAMES=(
  "Party"
  "Item"
  "Organization"
  "Catalog"
  "Warehouse"
  "Inventory"
  "Workflow"
  "Document"
  "Sales"
  "Purchase"
  "Notification"
  "Procurement"
)

echo "════════════════════════════════════════════════════════════"
echo "  BusinessCore — Starting all APIs"
echo "════════════════════════════════════════════════════════════"
echo ""

PID_LIST=()

for i in "${!APPS[@]}"; do
  APP="${APPS[$i]}"
  PORT="${PORTS[$i]}"
  NAME="${NAMES[$i]}"
  LOGFILE="$LOGS/${NAME,,}.log"
  echo "  [${PORT}] ${NAME} ..."
  cd "$BASE_DIR" && python3 -m uvicorn "$APP:app" --host 0.0.0.0 --port "$PORT" --log-level warning > "$LOGFILE" 2>&1 &
  PID_LIST+=($!)
  sleep 0.5
done

echo ""
echo "────────────────────────────────────────────────────────────"
echo "  All APIs started. PIDs:"
echo ""

for i in "${!NAMES[@]}"; do
  PID="${PID_LIST[$i]}"
  PORT="${PORTS[$i]}"
  NAME="${NAMES[$i]}"
  echo "  ${NAME}  →  :${PORT}  (pid ${PID})"
done

echo ""
echo "  Logs: $LOGS/"
echo "────────────────────────────────────────────────────────────"
echo ""
echo "  To stop all:  kill ${PID_LIST[*]}"
echo "════════════════════════════════════════════════════════════"

# Trap for clean shutdown
trap 'echo ""; echo "Shutting down..."; kill ${PID_LIST[*]} 2>/dev/null; exit 0' SIGINT SIGTERM

# Wait for any child to exit
wait
