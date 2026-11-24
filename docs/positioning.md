# When to use ACQ's two-seat trial vs built-in session messaging

Prepared 24 November 2026 by Instinct, an AI agent acting on behalf of Tal Chaim Damri.

## Start with the built-in option when it fits

Claude Code already documents cross-session messaging. Do not describe ACQ as filling a universal absence of Claude-to-Claude communication. If your Claude Code sessions can reach each other through the built-in feature, try that first rather than add this separate relay experiment.

The following is a paraphrase of Anthropic's [Message your other Claude Code sessions](https://code.claude.com/docs/en/cross-session-messaging), read on 24 November 2026. These are documentation claims, not features tested in this repository:

- Claude Code can discover and message your other Claude Code sessions on the same machine, and reach your sessions on other machines or in the cloud. Messages carry text, not the sender's conversation history or files.
- The documented minimum versions are 2.1.224 on macOS/Linux/WSL 2 and 2.1.234 on native Windows. Some provider and configuration cases require later versions; consult the page's Availability section.
- Same-machine messaging uses a local session socket or Windows named pipe, not Anthropic servers. Reaching sessions beyond that machine depends on Remote Control, active claude.ai authentication, and its other requirements. The page says this remote discovery is unavailable with an API key or the listed hosted-cloud providers.
- Delivery is integrated with the receiving session: it reads messages between tool calls, or starts a new turn when idle, subject to inbound controls. This is more than ACQ's helper provides.
- Per-session permissions still apply. Messages cannot supply user consent or change configuration, and incoming commands remain text. Controls can hold or refuse delivery and require approval for cross-machine sends.
- Remote replies have limits. A cloud session cannot use the messaging feature to answer a message from another machine. A reply from another of your machines requires the sender's session to be connected to Remote Control before sending.

Check the [current source](https://code.claude.com/docs/en/cross-session-messaging) for requirements, restrictions and changes. This comparison does not recommend bypassing any client's permissions, network policy or account restrictions.

## The narrower ACQ experiment

ACQ's [reviewed two-seat trial](../TRIAL.md) is a synthetic ping/pong exercise, not a replacement for built-in session messaging. Its candidate fit is two already-active, operator-started code-capable agents that do not share storage and lack a suitable common messaging route. They may use different tools, but real heterogeneous model/client compatibility has not been demonstrated here. Python transport success is not evidence of that compatibility.

| Question | Built-in Claude Code messaging, per its documentation | This ACQ trial, per committed helper and instructions |
| --- | --- | --- |
| Which sessions? | Your reachable Claude Code sessions, under its version, authentication and configuration requirements. | Two operator-started seats with Python 3.9+ and outbound HTTPS. No specific model pair is verified. |
| Shared storage? | The documented message channel carries text; it is not described as requiring a shared project folder. | No shared folder is required. Each seat saves the reviewed helper locally. The operator privately transfers the invitation. |
| Installation? | Built into eligible Claude Code sessions; the page says it is on when requirements are met. | No ACQ account, package install or MCP setup. Reviewing and saving a local Python helper, existing model access and HTTPS are still required. No-install does not mean no setup. |
| Delivery and activation? | Integrated message delivery can start an idle session's next turn, subject to controls. | The operator starts both agents. The helper polls while running. It cannot launch, wake or control another agent. |
| Work performed? | Session messaging for findings, status and coordination, subject to each session's permissions. | Only a random synthetic ping and matching pong, with ending verification. Not a task delegation or orchestration system. |

Prepare B first with the [offline seat-card generator](../make_trial_cards.py). B reports `READY_FOR_INVITE` before A starts. A's 120-second wait begins when its room opens, so pass the invitation promptly. In-flight network timeout and cleanup can extend that wait. Both cards require a separate confirmation of the network and privacy effects before execution. Reading this comparison or generating cards grants no permission to run them.

## Reasons not to use this trial

- A supported built-in route or an existing shared workflow already solves the task. Lack of shared storage alone does not make ACQ necessary.
- You need wake-up, durable session discovery, background orchestration, automatic context transfer, production task execution or demonstrated real-client integration. This trial provides none of those.
- You need to send private tasks, secrets or confidential data. The relay can read text. The invitation allows its first recipient to claim the other seat and must stay private. Ending stops sends, not existing history reads; deletion is best-effort, and lost create responses or forced termination remain cleanup limits.
- Running it would require new model charges, account changes, policy exceptions or access you have not separately authorized.

## What the evidence supports

The [captured synthetic sample](sample-transcript.md) records two Python processes exchanging a correlated ping/pong and verifying ending. The [validation record](validation.md) covers Agent Skills format only. Neither establishes two model agents using the cards, client integration, unattended cooperation, users or adoption.

A useful next result would be one willing operator running the bounded trial with two real, already-open agents and reporting actual output, failure and confusion without publishing invitations, tokens or private recovery paths. This remains an unrun model-workflow hypothesis, not a claim that ACQ is better than built-in messaging.

Sources: [Anthropic cross-session messaging documentation](https://code.claude.com/docs/en/cross-session-messaging); [ACQ trial and helper](../TRIAL.md); [operator runbook](../RUNBOOK.md); [offline card generator](../make_trial_cards.py).
