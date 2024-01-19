import run
from run import agent,render_it

for i in range(1000):
    score, s_list = render_it()
    print(f"Episode {i+1} has the score of: {score}")

    # After updating the agent:
    actor_loss_value = agent.actor_loss_value
    critic_loss_value = agent.critic_loss_value
    run.agent.write_summary(i, score, actor_loss_value, critic_loss_value)

    if i % 50 == 0 and i != 0:
        agent.save(f"checkpoint_{i}")