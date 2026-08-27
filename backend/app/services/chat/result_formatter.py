"""Result formatter — generates the narrative. Deliberately has NO parameter
for row data: real values never cross back into an LLM call. They flow
executor -> route -> JSON -> the UI's results table directly, matching the
"no data param — by design" boundary in the target architecture."""

from app.services.chat.sql_pipeline import GEMINI_MODEL, gemini_retry


@gemini_retry
def generate_answer(
    client, genai_types, question: str, row_count: int, columns: list,
    aggregate_values: dict | None = None,
) -> str:
    system_prompt = (
        "You answer questions about CSR project/donor data for the CSR Funding "
        "Portal. You are given the user's question, how many rows the query "
        "returned, which columns are in the result, and — only when the "
        "query was a plain aggregate (COUNT/SUM/AVG/MIN/MAX with no other "
        "columns) — the single computed aggregate value itself. You are "
        "never given individual row values. Write one short, natural-"
        "language sentence describing what was found, using the aggregate "
        "value verbatim when one is given, without inventing any other "
        "specific names, amounts, or values you were not given. If "
        "row_count is 0, say plainly that no matching data was found. Do "
        "not mention SQL, tables, or columns by their technical names — "
        "describe them in plain language."
    )
    user_content = (
        f"Question: {question}\n"
        f"Row count: {row_count}\n"
        f"Columns returned: {', '.join(columns) if columns else '(none)'}"
    )
    if aggregate_values:
        hint = ", ".join(f"{key} = {value}" for key, value in aggregate_values.items())
        user_content += f"\nComputed aggregate value(s): {hint}"

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=user_content,
        config=genai_types.GenerateContentConfig(
            system_instruction=system_prompt,
            max_output_tokens=200,
        ),
    )
    return response.text or ""
