# Reinforcement Learning

Reinforcement learning, or RL, is a type of machine learning where an agent learns by taking actions and receiving rewards or penalties.

Instead of learning from a fixed table of examples, the agent learns through interaction.

## Simple Definition

```text
agent takes action -> environment responds -> agent receives reward -> agent learns
```

## Key Terms

Agent:

```text
The learner or decision-maker.
```

Environment:

```text
The world the agent interacts with.
```

State:

```text
The current situation.
```

Action:

```text
What the agent chooses to do.
```

Reward:

```text
Feedback that says how good or bad the action was.
```

Policy:

```text
The agent's strategy for choosing actions.
```

## Example

Traffic signal timing can be framed as a reinforcement learning problem.

Agent:

```text
Traffic signal controller
```

State:

```text
Current queue lengths, waiting times, pedestrian calls, and traffic phase
```

Actions:

```text
Extend green, switch phase, or hold current phase
```

Reward:

```text
Lower delay, shorter queues, fewer stops, or safer crossings
```

The agent learns which signal actions tend to produce better rewards.

## How RL Differs From Supervised Learning

Supervised learning:

```text
Here are examples and correct answers. Learn to predict the answer.
```

Reinforcement learning:

```text
Try actions. Receive feedback. Learn a strategy that earns better rewards over time.
```

RL usually involves sequences of decisions. A good action now may help or hurt later.

## Exploration And Exploitation

Exploration means trying actions to learn more.

Exploitation means using the best-known action.

Example:

A traffic signal controller might try a new timing pattern to see if it reduces delay. But it should not explore recklessly if safety or reliability is at stake.

This tradeoff is central to reinforcement learning.

## When RL Is Useful

RL can be useful when:

- Decisions happen in sequence.
- Actions affect future states.
- A reward can be defined.
- Simulation is available for safe experimentation.

Transportation examples:

- Signal control in simulation
- Dynamic routing
- Fleet repositioning
- Transit dispatching
- Adaptive tolling simulations

## Strengths

- Learns decision strategies, not just predictions.
- Can optimize long-term rewards.
- Useful for control and operations problems.
- Works well in simulated environments.

## Limitations

- Can require many trials.
- Real-world exploration can be unsafe or expensive.
- Reward design is difficult.
- Learned policies can exploit flaws in the reward.
- Often more complex than needed for ordinary tabular prediction tasks.

## Common Mistakes

- Calling any AI decision system reinforcement learning.
- Ignoring the need for an environment and reward.
- Testing risky policies directly in the real world without simulation or safeguards.
- Designing a reward that misses safety, equity, or reliability concerns.

## Useful Links

- Sutton and Barto, Reinforcement Learning: An Introduction: http://incompleteideas.net/book/the-book-2nd.html
- OpenAI Spinning Up, RL introduction: https://spinningup.openai.com/en/latest/spinningup/rl_intro.html

