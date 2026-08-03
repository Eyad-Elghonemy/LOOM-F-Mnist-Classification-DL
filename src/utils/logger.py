"""
Logs every /classify call (success or failure) to the `predictions_log` table
in Supabase, so the frontend's Usage Analytics page has real data to read.

Logging failures are swallowed on purpose: a Supabase hiccup should never
break a prediction response for the end user. We just print a warning.
"""

from .config import SUPABASE


def log_prediction(
    success: bool,
    class_index: int | None = None,
    predicted_class: str | None = None,
    confidence: float | None = None,
) -> None:
    if SUPABASE is None:
        # No Supabase configured (e.g. local dev without the env vars) — skip silently.
        return

    row = {
        "success": success,
        "class_index": class_index,
        "predicted_class": predicted_class,
        "confidence": confidence,
    }

    try:
        SUPABASE.table("predictions_log").insert(row).execute()
    except Exception as e:
        # Don't let a logging failure take down the actual API response.
        print(f"[logger] Failed to log prediction to Supabase: {e}")
