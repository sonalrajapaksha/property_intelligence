# Entity resolution

Addresses are lowercased, punctuation and whitespace are normalized, and common street terms are abbreviated. Company suffix variants collapse to `ltd`. Original text remains on each raw observation.

Candidate generation uses the street number to limit comparison. A different street number, unit number or known postcode blocks a match. The weighted score uses address similarity (55%), locality (15%), land area (12%), building area (8%) and tenant name (10%). Missing signals are omitted and remaining weights are renormalized. This makes the score inspectable while retaining useful results from partial records.

At 93% or above a row matches automatically. From 75% to below 93% it enters manual review. Below 75% it becomes a distinct property. The manual queue permits Merge or Separate, and the selected state is saved.

Run `uv run python -m property_intel.evaluation` for precision, recall, F1 and false merge rate on six labelled regression cases. The set contains exact abbreviation matches, street-number conflicts, unit conflicts and different streets. Its size is far too small for statistical claims; new real-world error patterns should be added as labelled examples before tuning weights.
