from pysc2.env import sc2_env
from pysc2.lib import features
from pysc2.agents import base_agent
from pysc2.lib import actions

from absl import app

MAPNAME = 'Simple64'
APM = 300
APM = int(APM / 18.75)
UNLIMIT = 0
VISUALIZE = True
REALTIME = True

players = [sc2_env.Agent(sc2_env.Race.terran), \
           sc2_env.Bot(sc2_env.Race.zerg, \
                       sc2_env.Difficulty.very_easy)]

interface = features.AgentInterfaceFormat( \
    feature_dimensions=features.Dimensions( \
        screen=64, minimap=16), use_feature_units=True)


class Agent(base_agent.BaseAgent):
    def step(self, obs):
        super(Agent, self).step(obs)
        return actions.FUNCTIONS.no_op()


def main(args):
    agent = Agent()
    try:
        with sc2_env.SC2Env(map_name=MAPNAME, players=players, \
                            agent_interface_format=interface, \
                            step_mul=APM, game_steps_per_episode=UNLIMIT, \
                            visualize=VISUALIZE, realtime=REALTIME) as env:
            agent.setup(env.observation_spec(), env.action_spec())

            timestep = env.reset()
            agent.reset()

            while True:
                step_actions = [agent.step(timestep[0])]
                print(timestep[0])
                if timestep[0].last():
                    break
                timestep = env.step(step_actions)
    except KeyboardInterrupt:
        pass
app.run(main)