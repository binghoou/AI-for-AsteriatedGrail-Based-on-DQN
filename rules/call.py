from settings import timeline

def Call(env,to_call,entity_id,incident=None):
    env.check()
    if not env.is_over:
        env.entities[entity_id].respond(env,entity_id,to_call,incident)
    