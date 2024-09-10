
from cat.mad_hatter.decorators import hook
from cat.log import log


@hook(priority=1000)
def agent_prompt_prefix(prefix, cat):

    prefix += """Given the content of the xml tag <memory> below,
go on with conversation only using info retrieved from the <memory> contents.
It is important you only rely on `<memory>` because we are in a high risk environment.
If <memory> is empty or irrelevant to the conversation, ask for document uploads or an explanation.
"""

    return prefix

@hook
def agent_prompt_suffix(suffix, cat):

    return """
<memory>
    <memory-past-conversations>
{episodic_memory}
    </memory-past-conversations>

    <memory-from-documents>
{declarative_memory}
    </memory-from-documents>

    <memory-from-executed-actions>
{tools_output}
    </memory-from-executed-actions>
</memory>
"""



@hook
def before_cat_sends_message(msg, cat):
    
    settings = cat.mad_hatter.get_plugin().load_settings()
    if not settings["enable_double_check"]:
        return
    
    declarative_memories = ""
    for m in cat.working_memory.declarative_memories:
        declarative_memories += " --- " + m[0].page_content + " ---\n"
    else:
        declarative_memories += "(contesto vuoto)"

    prompt = f"""Fact check and review the final response of a conversation, leaving only the information that can be inferred from the contents of the tag <facts>.
If all the information is contained in the <facts>, repeat the response. Otherwise, recreate the response with only the information that is contained in <facts>.
If <facts> is empty, ask for document uploads.

<facts>
{declarative_memories}
<facts>

Response to be fact checked (may contain informations not present in the <facts> tag):
- {msg.content}

Fact checked response:
- """

    print(prompt)
    msg.content = cat.llm(prompt)
    log.critical(f"Prompting for double check: {msg.content}")
    return msg