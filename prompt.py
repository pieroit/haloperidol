
from cat.mad_hatter.decorators import hook
from cat.log import log


@hook(priority=1000)
def agent_prompt_prefix(prefix, cat):

    prefix = """Given the content of the xml tag <memory> below,
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
    return

    declarative_memories = ""
    for m in cat.working_memory.declarative_memories:
        declarative_memories += " --- " + m.page_content + " ---\n"
    else:
        declarative_memories += "(contesto vuoto)"

    prompt = f"""Devi editare la risposta finale di una conversazione, lasciando solo le informazioni che possono essere evinte dal CONTESTO.
Se tutte le info sono contenute nel CONTESTO, ripeti la risposta. Altrimenti, limita la risposta alle sole informazioni che non sono contenute nel CONTESTO.
Se il contesto è vuoto, chiedi di caricare documenti a riguardo.

CONTESTO:
{declarative_memories}

CONVERSAZIONE RECENTE E RISPOSTA:
{cat.stringify_chat_history()}
 - AI (risposta da editare): {msg.content}

RISPOSTA EDITATA:
"""

    msg.content = cat.llm(prompt)
    return msg