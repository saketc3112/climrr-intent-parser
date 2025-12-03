import re
from typing import Any, Dict
from ..utils.constants import FULL_KEY_MAP, get_final_data_key

# ---- Begin functions provided by user (logic preserved) ----

def process_query_with_clarification(user_query: str, input_data: Dict, turn_count: int = 0) -> Dict[str, Any]:
    """
    Manages the clarification loop based on parsed intent confidence and completeness.
    """
    user_query_lower = user_query.lower()
    intent = parse_raw_intent(user_query_lower)
    
    # If turn count limit not reached, perform validation checks
    if turn_count < 2:
        
        # 1. Variable Ambiguity
        if intent["variable"] and intent["variable_match_type"] == "ambiguous":
            return {
                "status": "clarification_needed",
                "message": f"Do you mean {intent['variable']}? Reply Yes or No."
            }
        
        # 2. Missing Variable
        if not intent["variable"]:
            options = [
                "Heating Degree Days", "Cooling Degree Days",
                "Average Maximum Temperature", "Average Minimum Temperature",
                "Wind Speed",
                "Fire Weather Index (95th percentile)", "Fire Weather Index (Class)",
                "Heat Index Days above 95F", "Heat Index Days above 105F", 
                "Heat Index Days above 115F", "Heat Index Days above 125F",
                "Daily Max Heat Index", "Seasonal Max Heat Index",
                "Days without Precipitation", "Total Precipitation", 
                "Average Daily Precipitation", "Maximum Daily Precipitation"
            ]
            return {
                "status": "clarification_needed",
                "message": f"I couldn't identify the specific climate variable. Available options include: {', '.join(options)}. Which one are you interested in?"
            }

        # 3. Missing Season
        if not intent["season"]:
            return {
                "status": "clarification_needed",
                "message": "Which season do you prefer for this question? Options are Annual, Winter, Spring, Summer, Autumn."
            }

        # 4. Missing Scenario details
        if intent["scenario_time"] != "Historical":
            if not intent["scenario_time"] or (intent["scenario_time"] != "Historical" and not intent["scenario_rcp"]):
                 return {
                    "status": "clarification_needed",
                    "message": "Which scenario and time period? Options: like historical, mid-century/end-century RCP4.5/RCP8.5? (for FIRE WEATHER INDEX and HEAT INDEX only RCP 8.5)"
                }

    # If we are here, we either have full intent OR we hit the turn limit (force fallback)
    msg_prefix = "Proceeding with current information... " if turn_count >= 2 else ""
    
    # Proceed to extraction (which handles applying defaults if still missing)
    result = extract_relevant_data(user_query, input_data, "")
    
    status = "fallback" if isinstance(result, list) else "success"
    message = msg_prefix + ("Full data provided." if status == "fallback" else "Relevant data extracted.")
    
    return {
        "status": status,
        "message": message,
        "data": result
    }

def parse_raw_intent(user_query_lower: str) -> Dict[str, Any]:
    """
    Analyzes the user query to extract variable, season, scenario and FWI subtype.
    Assigns confidence levels ('exact', 'ambiguous', 'missing') to the variable match.
    """
    intent = {
        "variable": None,
        "variable_match_type": "missing", # missing, exact, ambiguous
        "season": None,
        "scenario_time": None,
        "scenario_rcp": None,
        "fwi_subtype": None 
    }

    # --- 1. VARIABLE DETECTION ---
    
    # FWI Special Check
    if re.search(r"fire\s+weather|fwi\b", user_query_lower):
        intent["variable"] = "Fire Weather Index"
        intent["variable_match_type"] = "exact" # Treat FWI presence as exact intent base
        
        # Subtypes
        if re.search(r"95|percentile", user_query_lower): intent["fwi_subtype"] = "95"
        elif re.search(r"class|category|classification", user_query_lower): intent["fwi_subtype"] = "Class"
        elif re.search(r"average|avg", user_query_lower): intent["fwi_subtype"] = "Average"
        else: intent["fwi_subtype"] = "All"

    # Standard Variables
    if not intent["variable"]:
        known_vars = set(k[0] for k in FULL_KEY_MAP.keys() if k[0] != "Fire Weather Index")
        sorted_vars = sorted(known_vars, key=len, reverse=True)
        
        # Exact Match (Contiguous string)
        for var in sorted_vars:
            if var.lower() in user_query_lower:
                intent["variable"] = var
                intent["variable_match_type"] = "exact"
                break
        
        # Regex (Ambiguous/Fuzzy)
        if not intent["variable"]:
            regex_map = {
                "Average Maximum Temperature": [r"average\s+.*maximum\s+temp", r"avg\s+.*max\s+temp", r"max\s+avg\s+temp"],
                "Average Minimum Temperature": [r"average\s+.*minimum\s+temp", r"avg\s+.*min\s+temp", r"min\s+avg\s+temp"],
                # Robust detection for Days Without Precipitation to prevent overlap with "Precipitation" synonyms
                "Days Without Precipitation": [
                    r"days\s+without\s+precip", 
                    r"without\s+precip", 
                    r"without\s+any\s+precip", 
                    r"no\s+precip", 
                    r"days\s+without\s+rain"
                ]
            }
            for canonical, patterns in regex_map.items():
                for pat in patterns:
                    if re.search(pat, user_query_lower):
                        intent["variable"] = canonical
                        intent["variable_match_type"] = "exact" # Strong regex count as exact enough to skip clarifying
                        break
                if intent["variable"]: break

        # Synonym (Ambiguous)
        if not intent["variable"]:
            synonyms = {
                "rain": "Annual Precipitation", "precip": "Annual Precipitation",
                "dry": "Days Without Precipitation", "heat index": "Daily Max Heat Index", 
                "wind": "Wind Speed",
                "maximum": "Average Maximum Temperature", "max": "Average Maximum Temperature", "high": "Average Maximum Temperature",
                "minimum": "Average Minimum Temperature", "min": "Average Minimum Temperature", "low": "Average Minimum Temperature",
                "temp": "Average Maximum Temperature", # Most ambiguous fallback
            }
            sorted_syns = sorted(synonyms.keys(), key=len, reverse=True)
            for syn in sorted_syns:
                if syn in user_query_lower:
                    intent["variable"] = synonyms[syn]
                    intent["variable_match_type"] = "ambiguous"
                    break

    # --- 2. SEASON ---
    seasons = ["Winter", "Spring", "Summer", "Autumn", "Annual"]
    for s in seasons:
        if s.lower() in user_query_lower:
            intent["season"] = s
            break

    # --- 3. SCENARIO ---
    if "rcp 8.5" in user_query_lower or "8.5" in user_query_lower: intent["scenario_rcp"] = "RCP8.5"
    elif "rcp 4.5" in user_query_lower or "4.5" in user_query_lower: intent["scenario_rcp"] = "RCP4.5"
    
    if "end" in user_query_lower or "2100" in user_query_lower: intent["scenario_time"] = "End-Century"
    elif "mid" in user_query_lower or "2050" in user_query_lower: intent["scenario_time"] = "Mid-Century"
    elif "historical" in user_query_lower or "past" in user_query_lower: intent["scenario_time"] = "Historical"

    return intent

def extract_relevant_data(user_query, input_data, assistant_response):
    """
    Extracts data based on intent. Handles multiple scenarios if a comparison is detected.
    """
    user_query_lower = user_query.lower()
    results_data = input_data[0]['results'] if isinstance(input_data, list) and input_data else {}
    
    # Re-parse to get components (in production, we might pass the intent dict directly)
    intent = parse_raw_intent(user_query_lower)
    target_variable = intent["variable"]
    fwi_subtype = intent["fwi_subtype"]
    
    # Apply Defaults for extraction
    target_season = intent["season"] if intent["season"] else "Annual"
    
    # --- SCENARIO DETECTION LOGIC (Supports Comparison) ---
    scenarios_list = []
    
    # 1. Analyze Future Components from Query
    rcp_part = None
    if "rcp 8.5" in user_query_lower or "8.5" in user_query_lower: rcp_part = "RCP8.5"
    elif "rcp 4.5" in user_query_lower or "4.5" in user_query_lower: rcp_part = "RCP4.5"
    
    time_part = "Mid-Century" # Default future time
    if "end" in user_query_lower or "2100" in user_query_lower: time_part = "End-Century"
    
    # Construct potential future scenario string
    future_scenario_str = None
    if rcp_part:
        future_scenario_str = f"{time_part} {rcp_part}"
    elif "mid" in user_query_lower or "end" in user_query_lower or "project" in user_query_lower or "anticipate" in user_query_lower or "forecast" in user_query_lower:
        # Implied future if time words or predictive words exist, default to RCP4.5 if missing (unless variable logic suggests otherwise, but here generic)
        future_scenario_str = f"{time_part} {rcp_part if rcp_part else 'RCP4.5'}"

    # 2. Analyze Historical Component
    has_historical = re.search(r"historical|past|history|baseline", user_query_lower)
    
    # 3. Analyze Comparison Intent
    is_comparison = re.search(r"compare|contrast|difference|relative|vs\b|versus", user_query_lower)

    # 4. Build List
    if has_historical:
        scenarios_list.append("Historical")
        
    if future_scenario_str:
        scenarios_list.append(future_scenario_str)
        
    # 5. Handle Comparison Implication
    # If comparing and we have a future but no historical explicit, add historical (baseline)
    if is_comparison and future_scenario_str and "Historical" not in scenarios_list:
        scenarios_list.insert(0, "Historical")
        
    # 6. Fallback
    if not scenarios_list:
        scenarios_list.append("Historical")
        
    # Remove dupes and sort (Historical first preferred)
    scenarios_list = sorted(list(dict.fromkeys(scenarios_list)), key=lambda x: 0 if x == "Historical" else 1)

    # --- D. EXTRACTION LOGIC ---
    
    def extract_single_val(json_key, season, scen_str):
        actual_key = None
        for k in results_data.keys():
            if k.lower() == json_key.lower():
                actual_key = k
                break
        
        if not actual_key: return None
        
        var_block = results_data[actual_key]
        if season not in var_block: return None
        season_block = var_block[season]
        
        if scen_str == "Historical":
            if "historical" in season_block and "value" in season_block["historical"]:
                return season_block["historical"]["value"]
        else:
            rcp = "rcp85" if "RCP8.5" in scen_str else "rcp45"
            tm = "end_century" if "End-Century" in scen_str else "mid_century"
            if rcp in season_block and tm in season_block[rcp] and "value" in season_block[rcp][tm]:
                return season_block[rcp][tm]["value"]
        return None

    extracted_items = []
    
    # Iterate over all detected scenarios (e.g. Historical AND Mid-Century RCP8.5)
    for detected_scenario_str in scenarios_list:
        valid_base_key = get_final_data_key(target_variable, target_season, detected_scenario_str)
        
        if valid_base_key:
            # 1. Handle Fire Weather Index
            if target_variable == "Fire Weather Index":
                fwi_configs = [
                    {"type": "95", "json_key": "Fire Weather Index (95th Percentile)", "suffix": "_95"},
                    {"type": "Class", "json_key": "Fire Weather Index Class", "suffix": "_NC"},
                    {"type": "Average", "json_key": "Fire Weather Index (Average)", "suffix": "_Avg"}
                ]
                
                target_configs = fwi_configs if fwi_subtype == "All" else [c for c in fwi_configs if c["type"] == fwi_subtype]
                
                for config in target_configs:
                    val = extract_single_val(config["json_key"], target_season, detected_scenario_str)
                    if val is not None:
                        extracted_items.append({
                            "variable": config["json_key"],
                            "season": target_season,
                            "scenario": detected_scenario_str,
                            "csv_key": valid_base_key + config["suffix"],
                            "value": val
                        })
            
            # 2. Handle Standard Variables
            else:
                json_key_map = {
                    "Average Maximum Temperature": "Maximum Avg Temperature",
                    "Average Minimum Temperature": "Minimum Avg Temperature"
                }
                db_key = json_key_map.get(target_variable, target_variable)
                val = extract_single_val(db_key, target_season, detected_scenario_str)
                if val is not None:
                    extracted_items.append({
                        "variable": target_variable,
                        "season": target_season,
                        "scenario": detected_scenario_str,
                        "csv_key": valid_base_key,
                        "value": val
                    })

    if extracted_items:
        # Return list if multiple items found (comparison), or single dict if just one
        final_data = extracted_items if len(extracted_items) > 1 else extracted_items[0]
        return {
            "status": "success",
            "intent": {
                "variable": target_variable,
                "season": target_season,
                "scenario": scenarios_list # Return list of scenarios found
            },
            "extracted_data": final_data
        }

    return input_data

# ---- End functions (unchanged logic) ----

