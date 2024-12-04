from datetime import datetime
from typing import Dict, List
from app.models.points_models import Transaction, SpendPointsResponse
from app.core.data_store import data_store
from collections import defaultdict


async def _update_balance(payer: str, points: int) -> None:
    balances = await data_store.get("balances")
    balances[payer] = balances.get(payer, 0) + points
    await data_store.set("balances", balances)


async def _process_deduction(payer: str, points_to_deduct: int, transactions: List[Transaction]) -> None:
    remaining_deduct = points_to_deduct

    for transaction in transactions:
        transaction_payer = transaction["payer"]
        points = transaction["points"]
        
        if transaction_payer == payer and points > 0:
            available_points = points
            deduction = min(available_points, remaining_deduct)
            transaction["points"] -= deduction

            remaining_deduct -= deduction

            if remaining_deduct == 0:
                break

    await data_store.set("transactions", transactions)

async def _create_transaction(payer: str, points: int, timestamp: datetime) -> None:
    transaction = {
        "payer": payer,
        "points": points,
        "timestamp": timestamp.isoformat()
    }
    await data_store.append_transaction(transaction)


async def add_points(payer: str, points: int, timestamp: datetime) -> Dict:
    balances = await data_store.get("balances")
    transactions = await data_store.get("transactions")

    await _update_balance(payer, points)

    if points < 0:
        points_to_deduct = -points
        if balances[payer] < 0:
            return {"error": f"Not enough points for payer {payer}."}
        await _process_deduction(payer, points_to_deduct, transactions)
    else:
        await _create_transaction(payer, points, timestamp)

    return None


async def spend_points(points: int) -> List[SpendPointsResponse]:
    balances = await data_store.get("balances")
    transactions = await data_store.get("transactions")

    total_points = sum(balances.values())
    if total_points < points:
        raise ValueError("Not enough points to spend.")

    sorted_transactions = sorted(transactions, key=lambda x: x['timestamp'])
    points_to_spend = points
    spent_points = defaultdict(int)

    for transaction in sorted_transactions:
        payer = transaction['payer']
        points = transaction['points']
    
        if points_to_spend == 0:
            break
        if points <= 0:
            continue

        available_points = points
        deduction = min(available_points, points_to_spend)
        transaction['points'] -= deduction
        balances[payer] -= deduction
        spent_points[payer] -= deduction
        points_to_spend -= deduction

    await data_store.set("balances", balances)
    await data_store.set("transactions", transactions)

    return [SpendPointsResponse(payer=payer, points=points) for payer, points in spent_points.items()]


async def get_balance() -> Dict[str, int]:
    balances = await data_store.get("balances")
    return balances
