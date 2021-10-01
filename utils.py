
def print_train_info(time_step, state, epsilon, action, reward, q_max, loss):
    if q_max is not None:
        print("TIMESTEP", time_step, " STATE", state,
              " EPSILON", epsilon, " ACTION", action,
              " REWARD", reward,
              " Q_MAX %e" % q_max, " LOSS", loss.detach())
    else:
        print_simple_info(time_step, epsilon, action, reward)


def print_simple_info(time_step, epsilon, action, reward):
    print("TIMESTEP", time_step, " STATE", "observe",
          " EPSILON", epsilon, " ACTION", action,
          " REWARD", reward)
