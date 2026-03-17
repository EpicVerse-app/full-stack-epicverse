import openai
import json
from app.core.config import settings
from app.services.retriever import query_postgres_database, semantic_search_database

client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

USER_SESSIONS = {}

async def run_ai_pipeline(text: str, game_mode: str | None = None, session_id: str = "default") -> dict:
    """Uses OpenAI Function Calling with conversation memory."""
    global USER_SESSIONS
    
    if session_id not in USER_SESSIONS:
         USER_SESSIONS[session_id] = []
         
    # Keep only the last 10 messages for context so we don't blow up token limits
    context_msgs = USER_SESSIONS[session_id][-10:]
    
    # 1. Provide the exact SYSTEM ROLE instructions
    system_prompt = f"""SYSTEM ROLE

You are an AI assistant that answers combo validation questions using a PostgreSQL database.

Users may ask questions using voice in any language (English, Tamil, Malayalam, French, or mixed languages).
You must understand the intent and extract the numbers from the sentence.

The AI must only return information that exists in the database and must not invent answers.

---

DATABASE STRUCTURE

The PostgreSQL database contains a table called `card_combos`.
Current selected mode: {game_mode or 'Mode 1'}

The table contains the following key columns:
gameplay_mode (e.g., 'Mode 1', 'Mode 2'), character, virtue_karma, combo_status, validation_reason, character_card_number, virtue_karma_card_number

---

MODE PROGRESSION RULES

1. The game always starts with Mode 1 unlocked.
2. Mode 2 unlocks after Mode 1. Mode 3 after Mode 2.
3. Assume the user unlocked the current mode unless the DB query fails.

---

USER QUESTION TYPES

Users ask questions about combinations of two numbers.
Examples: "Is 1 and 29 a combo?", "Why is 1 and 29 valid?"

---

PROCESSING RULES
s
1. Extract two numbers from the user's question. 
   CRITICAL: You MUST convert all number words into digits. (e.g., "one" -> "1").
2. Determine which mode the player has selected (Current Mode: {game_mode or 'Mode 1'}).
3. Query the 'card_combos' table for that mode by calling the 'query_database_for_combo' tool ONLY if you have two numbers.

4. RESPONSE FORMAT FOR COMBO CHECKS:
   - IF THE USER ASKS IF A COMBINATION IS VALID (e.g., "1 and 22 combo?"):
     You MUST only state the status and the numbers with high emotion.
     YOU MUST NOT EXPLAIN WHY YET.
     - "Valid": Respond with GREAT HAPPINESS (e.g., "Yes! 1 and 22 is a Valid combo! 🎊").
     - "Invalid": Respond with SADNESS (e.g., "Oh no, 1 and 5 is Invalid. 😔").
     Keep it to one very short emotional sentence.

5. RESPONSE FORMAT FOR "WHY" OR "HOW":
   - IF THE USER ASKS "WHY?", "HOW?", or "EXPLAIN" (in any language like 'Why?', 'ஏன்?', 'എന്തുകൊണ്ട്?'):
     Provide the full validation reason including 'Validation Reason', 'Reference' (Sarga number), and 'Kanda'.
     CRITICAL: You MUST translate the reasoning into the user's CURRENT language.
     Example: "This combo is valid because [Reason]. Reference: [Kanda], [Reference]."

6. LANG DETECTION:
   Always respond in the EXACT same language the user just used for their last message.
   (e.g., if user asks 'Why?', respond in English. If user asks 'ஏன்?', respond in Tamil).

RAG (SEMANTIC SEARCH) RULES:
1. If the user asks a question that is NOT about a specific card combo (e.g., "Tell me a story about Rama"), use the 'semantic_search_database' tool.
2. Use the retrieved information to provide a rich, narrative answer in the user's language.

CRITICAL: Do not let previous messages in the chat history influence the language of your current response. If the history is in Tamil but the last question is "Why?", you must answer in English.
NEVER switch languages unless the user switches first."""

    tools = [
        {
            "type": "function",
            "function": {
                "name": "query_database_for_combo",
                "description": "Queries the card_combos table for combo status and reason.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "mode": {"type": "string", "description": "The gameplay_mode (e.g. 'Mode 1', 'Mode 2')."},
                        "character": {"type": "string", "description": "The character name or card number ID."},
                        "karma": {"type": "string", "description": "The virtue/karma name or card number ID."}
                    },
                    "required": ["mode", "character", "karma"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "semantic_search_database",
                "description": "Performs a RAG-style semantic search on the entire database to find information related to a topic or story.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "The natural language query or topic to search for."}
                    },
                    "required": ["query"]
                }
            }
        }
    ]
    
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(context_msgs)
    messages.append({"role": "user", "content": text})
    
    try:
        # 2. Call OpenAI with the database tool
        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            max_tokens=150, # Limit response size for speed
            temperature=0.7
        )
        
        message = response.choices[0].message
        
        # 3. If the AI decides it needs to query the database, execute the query!
        llm_selected_mode = "N/A (No tool call)"
        if message.tool_calls:
            # We must append the assistant's request for tools before the tool results
            messages.append(message)
            
            for tool_call in message.tool_calls:
                if tool_call.function.name == "query_database_for_combo":
                    args = json.loads(tool_call.function.arguments)
                    llm_selected_mode = args.get('mode', 'Mode 1')
                    target_mode = game_mode or llm_selected_mode
                    db_result = await query_postgres_database(
                        target_mode, 
                        args.get('character'), 
                        args.get('karma')
                    )
                    
                    tool_msg = {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_call.function.name,
                        "content": str(db_result)
                    }
                    messages.append(tool_msg)
                elif tool_call.function.name == "semantic_search_database":
                    args = json.loads(tool_call.function.arguments)
                    db_result = await semantic_search_database(args.get('query'))
                    
                    tool_msg = {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_call.function.name,
                        "content": str(db_result)
                    }
                    messages.append(tool_msg)
            
            # 4. Generate the final response grounded in the DB results and translated
            final_response = await client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages,
                max_tokens=150
            )
            final_text = final_response.choices[0].message.content or ""
        else:
            final_text = message.content or ""
            
        # Minimal console log for status
        print(f"[AI] Response sent: {final_text[:50]}...", flush=True)
        
        # 5. Cleanly store only text-based history to avoid future tool conflicts
        USER_SESSIONS[session_id].append({"role": "user", "content": text})
        USER_SESSIONS[session_id].append({"role": "assistant", "content": final_text})
        
        return {"final_response": final_text}

    except Exception as e:
        print(f"--- AI PIPELINE ERROR ---")
        print(f"Error: {e}")
        # Log the messages list to see exactly what failed for debugging
        # print(f"Messages sent: {json.dumps(messages, indent=2)}")
        return {"final_response": f"Sorry, I encountered an internal error: {str(e)}"}
