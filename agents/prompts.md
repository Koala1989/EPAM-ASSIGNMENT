# Agent prompts

Selected prompts from my Claude Code sessions (10–16 October 2026): the 96 of my 337 prompts that show how I directed the agents. That means designing and refining their instructions, the case formats and conventions, the duplicate rules, the project structure, and cutting tokens and run time. Routine prompts are left out (below). The instructions the agents work under are in [`system-instructions.md`](system-instructions.md).

## What is in this file

| Section | Contents |
|---|---|
| [Prompts by theme](#prompts-by-theme) | 96 prompts I typed, grouped by theme, in time order within each theme. Verbatim, typos included. |
| [Skill runs](#skill-runs) | All 35 skill commands I ran. They generated the test cases and the automation. |
| [How the agents are briefed](#how-the-agents-are-briefed) | The fixed prompts the skills send to each agent, and 4 early briefings written in full before the skills existed. |

**Left out:**
- routine operations: run this, delete that spec, mark cases approved, git, commands to run tests;
- questions about the generated code or tools ("what does this fixture do?"), and token or cost look-ups;
- prompts that fixed individual cases from review findings. The review files and each case's Review field record those changes;
- prompts for recording the demo videos;
- the other 112 agent prompts. They are the fixed prompts in the table below, with only the case IDs or paths changing.

**How it was produced.** [`tools/export_prompts.py`](../tools/export_prompts.py) reads the session transcripts in `~/.claude/projects/c--EPAM-Assignment/` and keeps the prompts listed in [`tools/prompts_selection.json`](../tools/prompts_selection.json). `python tools/export_prompts.py --all --out <file>` writes the full log instead: every prompt, skill command and agent prompt, by day. Pasted text up to 1,500 characters is kept whole; longer pastes are shortened, with their length noted, and demo passwords are masked. The planning before 10 October happened in a separate claude.ai chat and is not in the transcripts.

## Prompts by theme

| Theme | Prompts | What they show |
|---|---|---|
| [Requirements and knowledge base](#requirements-and-knowledge-base) | 9 | Pinning the docs to 1.5.6, a rule inventory per Area, and a local RAG index, with questions on how retrieval is scoped and kept current. |
| [Test case format and design rules](#test-case-format-and-design-rules) | 17 | The seed formats, Areas, the Review field, how open questions are written into cases, where each technique applies, cross-functional scope and data-driven cases. |
| [Agent instructions: writing and refining them](#agent-instructions-writing-and-refining-them) | 17 | Creating each agent, then tightening its instructions from what went wrong: guardrails, an assertion for every filled field, never inferring the opposite of a rule, missed negative cases, generator traces. |
| [Duplicate detection and independent review](#duplicate-detection-and-independent-review) | 9 | A scored duplicate checker, an LLM judge for borderline scores, merging the judge into a full reviewer, rule coverage checks and the log of what the reviewer caught. |
| [Orchestration and running the agents](#orchestration-and-running-the-agents) | 10 | From starting agents by hand to one skill per stage, many cases per run, unattended headless runs, and prompts that name only the functionality. |
| [Automation framework and conventions](#automation-framework-and-conventions) | 8 | The layered Playwright framework, real-form login, one config for UI and API, environments, and schema checks that report without hiding the other checks. |
| [Tokens, cost and speed](#tokens-cost-and-speed) | 11 | Cutting what the agents read and run: a heading index, Area-wise inventories, agent file size, prompt caching, skipping login runs, smaller page snapshots. |
| [Verification against the app and approval](#verification-against-the-app-and-approval) | 6 | Running cases through Playwright MCP and the API before approving them, automating only Approved cases, and turning a wrong assumption into a finding. |
| [Project structure and deliverables](#project-structure-and-deliverables) | 9 | CLAUDE.md, folder naming, one automation project, the submission documents, and keeping the case folders tidy. |

### Requirements and knowledge base

Pinning the docs to 1.5.6, a rule inventory per Area, and a local RAG index, with questions on how retrieval is scoped and kept current.

**1. 2026-10-10 05:30 UTC**

````text
Lets perform the step 3 first: Run P01 (requirements snapshot) to pull the versioned docs Markdown into requirements/docs/.
````

**2. 2026-10-10 17:14 UTC**

````text
yeah lets run P03 and create the requirements-inventory and also update the agent instruction accordingly. One question before implementing - would it make sense to create this file AREA wise to further reduce the token use ?
````

**3. 2026-10-11 10:49 UTC**

````text
could the reason behind these differences in doc and application found earlier be a result of us running 1.5.6 and not the latest ?
````

**4. 2026-10-12 16:28 UTC**

````text
Need to use a local RAG instead of requirements documents to fetch the requirement details - Tell me what we need ? how many places chnages would be needed ? and how much time ? Ask me the answers you need, do not assume
````

**5. 2026-10-12 17:51 UTC**

````text
Question: how about if we also use the RAG only to generate the requierment-inventory.md file ?
````

**6. 2026-10-12 17:56 UTC**

````text
but to create the rules for one area - lets say Part details, why would RAG cosine similarity look everywhere, why not just the specific Area in chromaDB ?
````

**7. 2026-10-12 18:00 UTC**

````text
ok one more quesiton what happens if in future the requirements change because of an enhancement- will I need to regenarte the whole embedding ?
````

**8. 2026-10-12 18:28 UTC**

````text
one question from the RAG topic- currently what is the top k and cosine similarity cut off ? and also tell me where it is mentioned so that I can see and update.
````

**9. 2026-10-14 17:38 UTC** · separate session

````text
I neeed to know waht details were provided by rag when it queried for creating 003
````

### Test case format and design rules

The seed formats, Areas, the Review field, how open questions are written into cases, where each technique applies, cross-functional scope and data-driven cases.

**10. 2026-10-10 07:24 UTC**

````text
next lets create a seed manual functional test case (for creating test cases) under references folder- it should have : summary, Link with the requirement, pre-requisites (i.e. which user ? any test data ? pre-steps etc), Steps for execution. Also suggest me anything else to be added.
````

**11. 2026-10-10 07:37 UTC**

````text
pre-requisites can be some times more than one liner, so will keep that but lets include - Tags: Smoke/Regression, Priority etc.
````

**12. 2026-10-10 07:54 UTC**

````text
instead of code use these instead: Part creation and import → Part
Detail view tabs → Detail_View
Categories → Categories
Attributes → ATT
Units of measure → Unit_measure
Revisions → REV
Parameters and templates/variants have their own areas in the docs → Part_Params, Part_Template
````

**13. 2026-10-10 16:55 UTC**

````text
Output files: should all cases go in one ui-manual-tests.md and one api-manual-tests.md, as the brief's deliverables suggest, or one file per functionality? -- No all different files put in different folders as per thier 'Area'.
Held questions: they're currently only in the agent's report. Should they also be saved to a file, for example test-cases/open-questions.md, so your answers are tracked? -- Ye s under output folder save them as open questions.
Requirements inventory: P03 hasn't been run, so cases cite doc lines without rule IDs. Run P03 first, or generate now? -- what was P03 ?
Known behaviour from the planning session: the agent works from the docs only, so it doesn't know about behaviour like duplicate IPN being allowed by default. Is that intended, with those cases surfacing as questions? we will handle this separately.
````

**14. 2026-10-11 05:53 UTC**

````text
yes lets add a review field in seed so that each generated test case gets it.
````

**15. 2026-10-11 11:57 UTC**

````text
si there any instruction that prohibits creation of a test case if a question is open ? becasue a test case shall always be created.
````

**16. 2026-10-11 11:59 UTC**

````text
we need to change that to - creat a test case but spcifically mention uder review - Open question. And if because of the question expected result is not clear then specifically mention that expected is not known becasue of the open question.
````

**17. 2026-10-13 05:30 UTC**

````text
I have reviewed soem questions and here is what i would suggest as changes: For any resource that doesn't exist if a GET/Delete operation is performed then it should return 404, please add an instruction in the agent also to keep non existing resources check and update the existing API test cases also
````

**18. 2026-10-14 18:11 UTC**

````text
I noticed when an open question is there then in that case it misses on writing the expected result also (as per the rule). I think then in that case at least expected should be filled as per the mentioned rule along with an open question,, what do you suggest
````

**19. 2026-10-14 18:38 UTC**

````text
one more question before we start- is equivalence partitioning really a testing technique or debugging/finding technique ?
````

**20. 2026-10-14 18:41 UTC**

````text
so then it should only apply to when there is a data input or dropdown value or API input to be provided .. correct ? not with the test users,, like in some case  test case generator has used to check for view only cases.
````

**21. 2026-10-15 15:29 UTC**

````text
see the requirement in assignment for automation ,, for third bulled suggest me a good test case we can automate.
````

**22. 2026-10-15 15:34 UTC**

````text
ok, lets create a new folder named cross functional scenario and put at least 5 such test cases in that folder by combining different test cases (flows) you may refer to the requriements to check what cross functional flows are there.
````

**23. 2026-10-16 07:28 UTC**

````text
next we need to include parametrized tets for API
````

**24. 2026-10-16 07:43 UTC**

````text
we need one correction, analyse first and suggest me,, don't make the chnages right away. Parametrization here means we need to run one spec agains a set of parameters for example - try to create a part with more than 100 chars, white space, empty name sould be one spec file running against different data set. Right now I see multiple test cases foe it instead of one parametrized test.
````

**25. 2026-10-16 07:49 UTC**

````text
one question: how it will be handled in the automated spec file,, will it have a loop or a datatable to run against and map outcome against each one ?
````

**26. 2026-10-16 08:32 UTC**

````text
I just regenerated the test cases and noticed it does not include the expected status code, lets add tone column for expected status code against each input.
````

### Agent instructions: writing and refining them

Creating each agent, then tightening its instructions from what went wrong: guardrails, an assertion for every filled field, never inferring the opposite of a rule, missed negative cases, generator traces.

**27. 2026-10-10 10:27 UTC**

````text
Now lets create an agent for manual test case creation that uses the seed from references for generation, include these sections: Objective, role, model, instruction (usual validations - Equivalence Partitioning and Boundary Value Analysis, State Transition and Decision Table Testing, Error Guessing and Exploratory Scenarios, negative cases, cases applicable for what if business scenarios). At the end once TC is drafted include the instruction to make the tool call for duplicate check and an LLM judging the final score if more than threshold. Desired flow will be like this -> User will call the prompt defining a functionality for Investree application for example: generate Test cases for Part creation flow, agent then will pull the context (rules and expected behavior) from the requirements. Raise if there is a conflict in the requirement i.e. contradictions or any open questions do not assume anything, add guardrails: to not assume anything. Use the further instructions to generate the test case using the seed template and finally assign a duplicate check score. If not duplicate and LLM judging is not needed then no need to mention the score as no score means unique. while creating the agent raise suggestions and questions and do not assume anything.
````

**28. 2026-10-11 04:58 UTC**

````text
will come to this later, also i see that the agent is missing the guardrails- what guardrails can be added ?
````

**29. 2026-10-11 17:21 UTC**

````text
Next we need to create a playwright test generator agent I have already copied one from one of my existing project, lets adjust this according to current project.
````

**30. 2026-10-12 06:10 UTC**

````text
I see base url is passed in generater agent, it should be only come from config file, also check the healer agent for same mistake
````

**31. 2026-10-12 06:34 UTC**

````text
Lets implement an indepnedent agent - that runs a review of the generated test for these: If the Conventions were followed or not, compare manually written test case and automated one should have all needed assertions and the test followed the SOLID coding priciples or not or anything thats part of standard playwright -typsescript coding practise. It should use a higher model than the generator or healer. finally saving the review file.
````

**32. 2026-10-12 08:26 UTC**

````text
I ran generation in another tab and got this as mentioned in the message. Question is if a page object is missing in page class then the generator agent will write it or not ?
````

**33. 2026-10-12 08:29 UTC**

````text
but if there are new page objects encountered then generator / healer shall update this I think.
````

**34. 2026-10-12 15:08 UTC**

````text
I noticed that not all fields are verified in test scripts after filling a form for example 

[pasted]
await test.step('2. Fill in the required field and the category only; leave IPN empty', async () => {
        await partForm.fill({ name: partName, category: String(category.name) });
        await expect(partForm.textField('name')).toHaveValue(partName);
        await expect(partForm.textField('ipn')).toHaveValue('');
        await expect(partForm.form.invalidFields).toHaveCount(0);
        await expect(partForm.form.formError).toBeHidden();
      });
[end of paste]

 is missing the category dropdown selection validation, which creates ambiguity. Lets make one correction in the generator agent to include expect for all the provided fields/driodown after filling a form. No need to rerun the and update the existing scripts.
````

**35. 2026-10-12 19:16 UTC**

````text
what do you suggest shallwe create separate agents for API test creation and automation or edit the same ones ?
````

**36. 2026-10-12 19:30 UTC**

````text
for automation lets create a separate agent for api automation, note that we will only use playwright and typescript for the API automation no separate tooling.
````

**37. 2026-10-14 16:20 UTC**

````text
for this prompt 'gen-test-cases UI Opening a part from the category list and the category breadcrumb' ,, it only generated positive test cases no negative ... why ?
````

**38. 2026-10-15 06:49 UTC**

````text
analyse all the blockers from the review catches file and suggest what can be improved in the generator agent ? analyse both closed as well as open and just suggest don't make changes.
````

**39. 2026-10-15 07:25 UTC**

````text
Lets start with the fix on #1 -  A guardrail against inferring the opposite (cause A, 3 Blockers).
````

**40. 2026-10-15 11:02 UTC**

````text
[pasted]
Two coverage additions from the same review are not done yet:

an invalid Link ("Enter a valid URL.") blocking submit;
a leading or trailing space in Name, and a Revision or Description of only spaces.
[end of paste]

  how come - these were missed when it si already mentioned to cover the ngative and invalid inputs in the generator agent instructiont ??
````

**41. 2026-10-15 11:09 UTC**

````text
check these now and just analyze why these might have happened in first place,, do we need to relax the guardrails ? 

[pasted]
Coverage gaps:
coverage_check.py shows all 9 SEC rules cited.
No 404 case is missing. The 404 cases for the {id} operations already exist in CRUD and REL.
The reviewer lists minor depth gaps:
R-SEC-01: no PATCH, PUT or DELETE and no category write without credentials. No positive case for session cookie or OAuth2.
R-SEC-04: no part-create positive that doesn't depend on an open question.
R-SEC-05: no positive PUT.
R-SEC-07: no positive category detail GET and no category PUT case.
R-SEC-08: the key case (Parts add granted, Purchase Orders add missing) is only API-SEC-044, whose outcome is not known.
Blocker, API-SEC-049:
It cites R-SEC-09, which says nothing about not-found.
It states the 404 body model name SupplierPart as fact, but that name is unconfirmed.
It repeats API-REL-035 and was never duplicate-checked against it.
[end of paste]
````

**42. 2026-10-15 13:35 UTC**

````text
I think there is an issue with generator as it faces some issues which results in multiple tool calls- like it  couldn't find seed file first and then at one point it just redirected briwser directly to 'web/part/category...' didn't add base url. I am attaching the traces from agent see why these issues are happpening what are possible fixes. Traces : Generate Playwright spec for UI-Part-001
Stopped · playwright-test-generator · Sonnet 5 · foreground
Spawned by the main agent
5m 45s · 145.1k tokens
Automate test case UI-Part-001.
6:43 PM
Automate test case UI-Part-001.
Grep "UI-Part-001" (in c:\EPAM_Assignment\test-cases)
4 lines of output
Read c:\EPAM_Assignment\automation\CONVENTIONS.md
Read c:\EPAM_Assignment\test-cases\Part_Creation_and_Import\part-creation-flow.md
Read c:\EPAM_Assignment\automation\reviews\ui\ui-part-001-review-2026-10-15.md
Read c:\EPAM_Assignment\automation\fixtures\index.ts
Read c:\EPAM_Assignment\automation\pages\part-form.page.ts
Read c:\EPAM_Assignment\automation\pages\part-detail.page.ts
Read c:\EPAM_Assignment\automation\pages\parts.page.ts
Read c:\EPAM_Assignment\automation\fixtures\data.fixture.ts
Read c:\EPAM_Assignment\automation\pages\components\f
[… 48,856 more characters of pasted output omitted]
````

**43. 2026-10-16 09:56 UTC**

````text
one question - we changed the healer invocation: now it should only runs if the generator reports a failure. My question is - is generator performing a dry run ?
````

### Duplicate detection and independent review

A scored duplicate checker, an LLM judge for borderline scores, merging the judge into a full reviewer, rule coverage checks and the log of what the reviewer caught.

**44. 2026-10-10 09:27 UTC**

````text
also need to include a score based duplicate checker which detects each test case's uniqueness and assigns a unique check. Suggest me if this should be a script or an LLM action ?
````

**45. 2026-10-10 09:44 UTC**

````text
the duplicate check script will only be used by the test cases creater agent once the test case is created and saved, a duplicate score will be saved at the last that can be then assessed by LLM in case the duplicate score is between 50-80 with the list of test cases file in reference that have a  match.
````

**46. 2026-10-10 17:35 UTC**

````text
Independent judge: the agent judges duplicates among the cases it just wrote, which is a biased check. A subagent can't start another subagent, so for an independent judge, run a second pass with Copilot or a separate agent.- Question: where is the subagent ? I only see one agent -test-case-creator.md
Technique field: add a Technique field to the seed, so each case shows which design technique produced it, not just the coverage table.
Submission copy: the brief expects agent config under agents/, so copy this file there when you submit, or explain its location in the README. - Implement this.
````

**47. 2026-10-10 17:41 UTC**

````text
for judging the duplicate check, lets implement another agent that acts independently -LLM as judge.
````

**48. 2026-10-11 11:50 UTC**

````text
review all the test cases recently generated for revisions and check if all the rules mentioned in 'requirements-inventory.md' of revisions are covered in test cases.
````

**49. 2026-10-13 17:13 UTC**

````text
I was wondering if we add more than just one validation to the duplicate-judge agent, like it should act as on overall reviewer and not just duplicate check. For example it should check that all rules are covered, by cross checking the requirement inventory.
````

**50. 2026-10-13 17:21 UTC**

````text
Lets merge them anyways and put a condition that duplicacy check verification only run when the score crosses 50 ,, which means for the demo work it will likely not run and will go to the other review process.
````

**51. 2026-10-15 03:54 UTC**

````text
Lets first investigate why some rules were not covered in any of the test cases from 'UI Part parameters tab parameter templates and category parameters'
````

**52. 2026-10-15 06:02 UTC**

````text
I want to create a notes list where I want to record the misses made by generator and then were discovered by reviewer along with a very short description why it might have been missed. This will help in improving as well as showing to interviewers about reviewers significance.
````

### Orchestration and running the agents

From starting agents by hand to one skill per stage, many cases per run, unattended headless runs, and prompts that name only the functionality.

**53. 2026-10-11 06:04 UTC** · separate session

````text
Use the test-case-creator agent to generate UI test cases for the Part creation flow.
````

**54. 2026-10-11 08:19 UTC**

````text
I am thinking of having an orchestration for the two agents so that they can be run from 1 trigger
````

**55. 2026-10-11 08:24 UTC**

````text
ok, lets create the skill now that calls both one by one
````

**56. 2026-10-12 07:10 UTC** · separate session

````text
Use the playwright-test-generator agent to automate test cases from PART area.
````

**57. 2026-10-12 18:30 UTC**

````text
Need ot create skill for automation that runs all agents - generator, healer, reviewer. Create a separate skill don't add to existing generate test cases skill.
````

**58. 2026-10-12 18:46 UTC**

````text
what if I need to run automation generation for entire Area/multiple Tcs in future
````

**59. 2026-10-13 06:43 UTC**

````text
lets also create a separate skill for automation of API including automation and review agents
````

**60. 2026-10-13 06:47 UTC**

````text
generate all alternatives to run skills and individual agents I will document in the submission
````

**61. 2026-10-14 18:27 UTC**

````text
now I am going to run this in terminal to run over night,, confirm if it looks ok or anything to change. -- 

[pasted]
$runs = @(
  'UI Part detail view header and tab visibility (Allocated, Build Orders and other tabs)',
  'UI Part detail view Stock tab',
  'UI Bill of materials tab editing and validation',
  'UI Test templates tab',
  'UI Attachments and Related Parts tabs',
  'UI Part parameters tab and parameter templates',
  'UI Category hierarchy, filtering and parametric tables',
  'UI Template parts and the Variants tab',
  'UI Part creation form validation, duplicate IPN and initial stock'
)
$log = "agents/runs/overnight-$(Get-Date -Format yyyy-MM-dd)"
New-Item -ItemType Directory -Force $log | Out-Null
$tools = 'Read,Grep,Glob,Edit,Write,Agent,' +
         'Bash(python tools/dedupe_cases.py *),' +
         'Bash(python tools/coverage_check.py *),' +
         'Bash(tools/rag/.venv/Scripts/python.exe tools/rag/query_index.py *)'
$i = 0
foreach ($r in $runs) {
  $i++
  $name = '{0:D2}-{1}' -f $i, ($r -replace '[^A-Za-z0-9]+', '-').ToLower()
  "$(Get-Date -Format HH:mm) start $r" | Tee-Object -Append "$log/summary.txt"
  claude -p "/gen-test-cases $r" --permission-mode acceptEdits --allowedTools $tools *> "$log/$name.md"
  "$(Get-Date -Format HH:mm) end   $r (exit $LASTEXITCODE)" | Tee-Object -Append "$log/summary.txt"
}
[end of paste]
````

**62. 2026-10-16 09:02 UTC**

````text
is it not possible to group them in 2-3 broader prompts becasue as of now it looks like I need to tell the scenarios from promot
````

### Automation framework and conventions

The layered Playwright framework, real-form login, one config for UI and API, environments, and schema checks that report without hiding the other checks.

**63. 2026-10-12 03:45 UTC**

````text
don't make changes just asking: is the generator and healer agent aware of a good playwright framework conventions such as page object, common utils script, a base page for common inventree patterns?
````

**64. 2026-10-12 05:11 UTC**

````text
Yes we need to make a conventions.md- create a draft and I will review. Lets implement above standards in these layer- 1. Test Layer -  Contains actual test scripts (*.spec.ts or *.spec.js). These files should contain minimal logic and read like business requirements, focusing primarily on the workflow execution and assertions. 2. Page Object Model Layer (pages/): Encapsulates the UI elements (locators) and behavior (actions like clicking, typing, or navigating) for individual pages. Tests interact with these classes rather than querying raw DOM elements directly, 3. Fixtures Layer (fixtures/): Manages shared setup and teardown logic, browser contexts, and authenticated states (storageState). Custom fixtures inject page objects or API states directly into tests, cutting out repetitive boilerplate code. 4. Utility Layer (utils/): Contains stateless helper functions such as custom date formatters, database clients, custom loggers, or string generators. 5. Data & Configuration Layer (data/ & config/): Decouples environment-specific URLs, timeouts, secret variables, and test input matrices (JSON/CSV files) from the executable code (I think playwright.config.ts is the right file for this purpose). Lets make a plan to implcment these so that I can review before implementing
````

**65. 2026-10-12 15:52 UTC**

````text
It doens't mimic an actual user so we will need to change that and use real login like a normal user would, before we make that chnage lets pull from everywhere where a change will be needed.
````

**66. 2026-10-13 08:23 UTC**

````text
I tried running api automation skill again and got this response this time, check if there is a defect which is causing this : 

[pasted, 2,807 characters; starts: "I've paused at 8 of 26 because one finding keeps blocking the cases, and handling it is your decision as architect. **What's happening:** a part created without a category comes back without `category_name`, which the `Part` schema lists as required. So far 5 specs are marked `fi…"]
````

**67. 2026-10-13 09:32 UTC**

````text
but that's a defect if API schema says it must be present and it is entirely missing
````

**68. 2026-10-13 09:33 UTC**

````text
yeha only schema failure should report failure other assertions must stay as it is
````

**69. 2026-10-13 11:50 UTC**

````text
there is one more issue in general, the UI and API projects are seggregated. How can a global config file be used for both which sets variables such as environment (accordingly test users are initialized), BaseURL for both API and UI tests
````

**70. 2026-10-14 14:12 UTC**

````text
lets include env files for web version also so that I can show that in demo as well
````

### Tokens, cost and speed

Cutting what the agents read and run: a heading index, Area-wise inventories, agent file size, prompt caching, skipping login runs, smaller page snapshots.

**71. 2026-10-10 06:24 UTC**

````text
i need to reduce the token usage when querying- can you suggest how token uage can be reduced while querying the reqirements for further use
````

**72. 2026-10-10 06:25 UTC**

````text
Add a heading index now.
````

**73. 2026-10-10 17:53 UTC**

````text
Just suggest don't make any changes: I see test case creator agent is 2000+ words, will it take too much tokens ?? what can be done ?
````

**74. 2026-10-12 18:01 UTC**

````text
New topic - Need to implement the prompt caching
````

**75. 2026-10-12 18:13 UTC**

````text
one question - you mentioned 'The dry run confirms caching is working as expected, with ~90% of each prompt served from cache after the first call, and the RAG CLI still functions post-refactor. Next, I'll write documentation covering caching for the Claude Code agents and how to run the API pipeline.' how did the dry run work without an APi key ?
````

**76. 2026-10-12 18:20 UTC**

````text
but the draft_cases_cached.py only contians certain instructions and rule,, not conventions or seed files
````

**77. 2026-10-12 18:22 UTC**

````text
just asking - what if only choose first cahcing option  (without key and sdk) how much token cost saving would there be ?
````

**78. 2026-10-15 12:39 UTC**

````text
I see one issue- whenever healer or automation generator runs then to tets the generated test it starts running all logins as well,, I think it is not needed. Also suggest me what other ways we can fast up the automation generation
````

**79. 2026-10-15 14:15 UTC** · separate session

````text
so if we call the skill repeatedly then the agent cache would still be hot and every subsequent generation will be served from cached prompts ?
````

**80. 2026-10-15 14:19 UTC**

````text
test case automation took 140K tokens, any possibility we can reduce the token usage,, let me know if you need the full trace
````

**81. 2026-10-15 14:23 UTC**

````text
so for 2 - I want to understand why the full page snapshot is needed ? is it because it needs full html dom to find locators
````

### Verification against the app and approval

Running cases through Playwright MCP and the API before approving them, automating only Approved cases, and turning a wrong assumption into a finding.

**82. 2026-10-11 06:31 UTC**

````text
Just now I generated the test case for part creation flow and it raised some questions , can you review once if they are valid and what is the right explanation for each of them
````

**83. 2026-10-11 07:13 UTC**

````text
before I mark these test cases as approved, lets add the playwright MCP to the project and run these test cases manually via MCP.
````

**84. 2026-10-11 07:15 UTC** · separate session

````text
[pasted]
Using the Playwright MCP, execute the 6 test cases in test-cases/Part/part-creation-flow.md
against http://localhost/web, exactly as written.

- Create each case's prerequisite data first as admin via the API
  (http://localhost/api/, token from /api/user/me/token/), with names QA-<8 random hex>.
- Run each step as the case's user, compare actual vs expected at every step,
  and take a screenshot at each expected-result check.
- Record results in test-cases/Part/runs/2026-10-11-part-creation-flow.md:
  per case Pass / Fail / Blocked, and for each failed step the expected vs actual result.
- Do not edit the test cases or their Review field. If a step can't be followed as written
  (label, menu or field differs from the case), mark it a case defect in the run log.
- Clean up afterwards as admin: make the created parts inactive, delete them,
  then delete the category and companies.
[end of paste]
````

**85. 2026-10-13 05:13 UTC**

````text
there are some open questions for CRUD API tests can you perform the API calls and confirm when the scenarios in questions are performed ?
````

**86. 2026-10-14 18:24 UTC**

````text
for now lets keep the automation check till review field only- if it is approved then automate
````

**87. 2026-10-15 16:43 UTC**

````text
change the pre-requisite to use all access and record this as a defect in findings. Also tell me the requirement that says an engineer can create stock
````

### Project structure and deliverables

CLAUDE.md, folder naming, one automation project, the submission documents, and keeping the case folders tidy.

**88. 2026-10-12 18:53 UTC**

````text
Need to include a claude.md file
````

**89. 2026-10-13 03:53 UTC**

````text
Lets create a prefix 'API_' to the folder names having API test and make the updates in all the references that use it
````

**90. 2026-10-14 07:59 UTC**

````text
I see we are running two projects - one for UI automation and another for API. Ideally it should be one automation project.
````

**91. 2026-10-14 13:24 UTC**

````text
test cases folder names are a bit confusing, instead rename them to full names like ATT to Attribute, and also update all the references where they are called.
````

**92. 2026-10-16 07:03 UTC**

````text
chekc the assignemtn document and suggest what is missing in the documentation
````

**93. 2026-10-16 07:25 UTC**

````text
now lets create this: README.md at the root: setup, tool choices, approach summary
````

**94. 2026-10-16 08:42 UTC**

````text
Meanwhile generate this file -	agents/system-instructions.md as per the rquirement of the assignment.
````

**95. 2026-10-16 11:00 UTC**

````text
Need to fix one thing - there is a lot of clutter under the each area test cases folder lets move all open questions to a common Open questions folder with names like open-question_<AREA>.md, similarly move the review comments under the same folder.
````

**96. 2026-10-16 11:06 UTC**

````text
are the agents also updated accordingly ?
````

## Skill runs

Every skill command, in order. Each one ran the agents for one stage: test cases, UI automation or API automation.

| Date (UTC) | Command |
|---|---|
| 2026-10-11 08:39 | `/gen-test-cases UI Part revisions` |
| 2026-10-13 03:22 | `/gen-test-cases API Part and category CRUD` |
| 2026-10-13 09:55 | `/automate-api-cases API-CRUD-009,API-CRUD-010,API-CRUD-011,API-CRUD-012,API-CRUD-0013,API-CRUD-014` |
| 2026-10-13 17:54 | `/gen-test-cases UI Part Import,  ATT, Categories, Detail_View, Part_Template` |
| 2026-10-14 06:38 | `/gen-test-cases UI Unit_measure` |
| 2026-10-14 11:10 | `/gen-test-cases UI Part_Params` |
| 2026-10-14 14:04 | `/gen-test-cases API FIELD_Validation, Lists_and_Filters, Relationships` |
| 2026-10-14 16:08 | `/gen-test-cases UI opening a part from the categaory list and  the category breadcumb` |
| 2026-10-14 18:36 | `/gen-test-cases UI Part parameters tab parameter templates and category parameters` |
| 2026-10-14 19:08 | `/gen-test-cases UI Bill of materials tab editing and validation` |
| 2026-10-15 04:28 | `/gen-test-cases UI Parameter unit validation setting and selection list administration` |
| 2026-10-15 04:38 | `/gen-test-cases UI BOM consumable optional and substitute lines multi-level BOMs BOM import comparison and component replacement` |
| 2026-10-15 04:56 | `/gen-test-cases UI Part detail view header details and tab visibility including the Allocated and Build Orders tabs` |
| 2026-10-15 05:26 | `/gen-test-cases UI BOM tab contents and visibility quantity calculations multiple substitutes and Excel import` |
| 2026-10-15 05:29 | `/gen-test-cases UI Return Orders Transfer Orders and Test Results tab visibility` |
| 2026-10-15 06:28 | `/gen-test-cases UI Category hierarchy filtering and parametric tables with unit-aware filtering and sorting` |
| 2026-10-15 06:45 | `/gen-test-cases UI Test templates tab` |
| 2026-10-15 07:33 | `/gen-test-cases UI Template parts and the Variants tab` |
| 2026-10-15 08:08 | `/gen-test-cases /gen-test-cases UI Test templates cascading from a template part to its variants' stock items` |
| 2026-10-15 08:47 | `/gen-test-cases UI Attachments and Related Parts tabs` |
| 2026-10-15 08:56 | `/gen-test-cases UI BOM consumable optional and substitute lines BOM import comparison and component replacement` |
| 2026-10-15 09:41 | `/gen-test-cases UI Part detail view Stock tab` |
| 2026-10-15 10:04 | `/gen-test-cases UI Part creation initial stock (Create Initial Stock setting and section)` |
| 2026-10-15 10:11 | `/gen-test-cases UI Part creation form validation (form errors block submit, unique name, description, revision, IPN)` |
| 2026-10-15 10:28 | `/gen-test-cases UI Part creation form validation: invalid Link URL, leading/trailing whitespace in Name, whitespace-only Revision and Description` |
| 2026-10-15 10:55 | `/gen-test-cases API Security and permissions: authentication and role permissions on parts, categories and supplier parts` |
| 2026-10-15 11:16 | `/gen-test-cases API Conflict scenarios: duplicate name/IPN/revision, duplicate category name under one parent, deleting a part in use` |
| 2026-10-15 12:24 | `/automate-cases UI-Part-001` |
| 2026-10-15 13:41 | `/automate-cases UI-PART-001` |
| 2026-10-15 16:52 | `/automate-cases UI-XF-001` |
| 2026-10-16 08:06 | `/gen-test-cases API Part name validation on create` |
| 2026-10-16 08:51 | `/automate-api-cases API-VAL-087` |
| 2026-10-16 10:09 | `/gen-test-cases UI Part creation with only the required fields` |
| 2026-10-16 10:32 | `/automate-cases UI-Part-074` |
| 2026-10-16 11:20 | `/gen-test-cases API Part field validation on create and update` |

## How the agents are briefed

The skills send short, fixed prompts on purpose: each agent reads its instructions from its own file, and reviewers get only IDs or paths, never another agent's reasoning.

| Skill | Agent | Prompt |
|---|---|---|
| `/gen-test-cases <UI\|API> <functionality>` | `test-case-creator` | `Generate <UI\|API> test cases for <functionality>.` |
| | `test-case-reviewer` | `Review <UI\|API> test cases for <functionality>: <every case ID created>.` |
| `/automate-cases <case IDs>` | `playwright-test-generator` | `Automate test case <case ID>.` |
| | `playwright-test-healer` (only if lint, types or the first run fail) | `Run and stabilise <spec path>.` plus any lint and type errors |
| | `playwright-test-reviewer` | `Review <spec path>.` |
| `/automate-api-cases <case IDs>` | `api-test-generator` | `Automate test case <case ID>.` |
| | `api-test-reviewer` | `Review <spec path>.` |

Agent prompts in the transcripts: 116 (`test-case-creator` 37, `test-case-reviewer` 31, `api-test-generator` 15, `api-test-reviewer` 14, `playwright-test-generator` 10, `playwright-test-reviewer` 4, `playwright-test-healer` 3, `duplicate-judge` 1, `claude-code-guide` 1). `duplicate-judge` was later merged into `test-case-reviewer`.

### Early briefings, before the skills

On 11 and 12 October the agents were started with prompts written in full. They carried context that later moved into the agent files, which is why the skills' prompts are now one line.

**`test-case-creator`, 2026-10-11 06:04 UTC**

````text
Generate manual functional UI test cases for the InvenTree Parts functionality "Part creation flow". Use the project's reviewed requirements inventory (test-cases/<Area>/requirements-inventory.md for the Parts area) and the version-pinned docs it cites, following the format in references/seed-manual-test-case.md. Focus on UI test cases (user-facing flows in the web interface). Follow your standard process: raise requirement conflicts and open questions instead of assuming, hold affected cases, run the duplicate check, and hand borderline matches to duplicate-judge as your instructions describe.

In your final report include: the file path(s) where cases were saved, the number of cases created (and IDs/titles), any held cases and why, all open questions/requirement conflicts raised, duplicate-check results (and whether duplicate-judge was run and its outcome), and any problems encountered (e.g. missing inventory file).
````

**`playwright-test-generator`, 2026-10-12 07:10 UTC**

````text
Automate the Approved manual test case UI-Part-001 ("Create a part with only the required fields") from test-cases/Part/part-creation-flow.md into a Playwright spec under automation/ui/tests/Part/, following automation/ui/CONVENTIONS.md and using the existing page objects and fixtures. Execute the steps live in the browser first. If a page object lacks a needed locator or action, stop and report exactly what is missing. In your final report, give: the spec file path written, whether it passed, any page-object gaps, and any differences you saw between the app and the case.
````

**`playwright-test-healer`, 2026-10-12 08:27 UTC**

````text
Run the generated Playwright UI specs in automation/ui/tests/Part/ (ui-part-001 through ui-part-005; ui-part-006 does not exist yet, ignore it). Debug any failures and fix how each test runs (locators in page objects, waits, fixture usage, test data) without changing what it checks, following automation/ui/CONVENTIONS.md. If InvenTree behaves differently from the Approved manual case in test-cases/Part/part-creation-flow.md, mark the test fixme with the evidence instead of changing the assertion.

Notes from the generator, worth checking if they fail:
- 001: partForm.fill picks the category via SelectComponent.select; make sure it selects the option, not the text echoed in the input. Step 4 asserts the IPN row has count 0 (app hides the row when IPN is empty).
- 003: toHaveCount(0) on the Add Parts button can pass before the toolbar renders; tighten the wait in PartsPage.open() if flaky.
- 004: the IPN/Keywords comparisons derive <suffix> from data.name's QA-<hex> prefix; Link uses toHaveText (switch to toContainText if needed).
- 005: supplier field visibility assertion may fail if the section starts collapsed.

Also run lint and type check if the project has them. In your final report give, per spec: pass/fail, what you changed (file and reason), anything marked fixme with evidence, and the final run result. Clean up any test data you create.
````

**`playwright-test-reviewer`, 2026-10-12 09:56 UTC**

````text
Review all the automated Playwright UI specs in automation/ui/tests/Part/ (ui-part-001 through ui-part-006), one review per spec, saved in automation/ui/reviews/ per your instructions. Check each against automation/ui/CONVENTIONS.md, its Approved manual case in test-cases/Part/part-creation-flow.md (every step and every Expected result asserted), SOLID, and standard Playwright + TypeScript practice. Run lint and type check (npm run lint, npm run typecheck in automation/ui).

Context you should know:
- 006 relies on two new locators I added to automation/ui/pages/part-detail.page.ts (supplierPartsTable, manufacturerPartsTable, via a private accordionSection helper); review that change as part of 006.
- Run history: 002/004/005 passed every run; 001 failed once in about 8 runs (cause unknown, error output lost); 006 failed once in 8 (allaccess page still loading when BasePage.goto's 10 s navigation-menu check timed out); 003 passed but its toHaveCount(0) check on the Add Parts button could pass before the toolbar renders.
- Do not edit any code. In your final report, give per spec: verdict, findings by severity, and the review file path; then a short cross-cutting summary.
````

**`test-case-reviewer`, 2026-10-16**

````text
Review API test cases for Part field validation on create and update: API-VAL-092, API-VAL-093, API-VAL-094, API-VAL-095, API-VAL-096, API-VAL-097, API-VAL-098, API-VAL-099, API-VAL-100, API-VAL-101, API-VAL-102, API-VAL-103, API-VAL-104, API-VAL-105, API-VAL-106, API-VAL-107, API-VAL-108.
````

Review file: `test-cases/Reviews/VAL_part-field-validation-on-create-and-update-review-2026-10-16.md` · Verdict: Changes required.
