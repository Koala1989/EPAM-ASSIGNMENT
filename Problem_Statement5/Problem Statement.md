Problem Statement : Improving Test Coverage and Risk Management for an Insurance

Claims Processing Platform

Background:

**Team outlook:**

| **Teams**              | **dev** | **QA** | **Testing Strategy** |
|------------------------|---------|--------|----------------------|
| Platform - 3           | 6       | 3      | Automated            |
| Product - 3            | 6       | 3      | Untracked            |
| Data Integration/E2E-2 | 4       | 2      | Untracked            |

**Risk Areas (based on the Production Incident):**

- Integrations: Likely lacking Contract testing.

- Claim calculation error: Likely caused due to low test coverage issues in product testing.

**Below will be my proposed plan**

**Step – 1 Analyse:**

- Start with Incidents – Review if there are any test cases already in place for the issues reported. Review and check all the business rules for calculation are covered in the test cases.

- Is Documentation on different claim journeys starting with happy flows available.

- Integration scenarios- Analyse what is causing under testing of integrations, some usual challenges are:

  - Insufficient test data in lower SIT/UAT env.

  - Unavailability of upstream/downstream systems or teams.

- What is the impact of 50% prod incidents. Calculate a risk score Likelihood X Impact.

**Step – 2 Plan/change in operating model:**

- <u>Utilize QAs help from platform team to setup contract testing using PACT</u>, API automated and service virtualization if the systems are not available. As they already have automation tests running nightly builds.

- <u>Have an impact analysis</u> per user story during refinement, in addition an AI agentic setup can be used to calculate the blast radius.

- <u>Check if Production incidents related scenarios were tested</u>, if not add a test case to regression and review with team for more possible failing scenarios. As this is opportunity to find related issues before more incidents appear.

- Make test cases tracking and linking with requirement a mandatory process and have a metrics around it.

- Document the happy path flows for claim processing and run it using a golden dataset from production data (masked).

- Track the results in each environment before going live each sprint (biweekly)

**Step-3 Executions & Optimizations**

Follow below execution plan each release:

- *<u>On Feature merge deployment</u>*: On merges of new features, trigger rules tests using golden dataset to ensure claims processing is happening correctly.

- *<u>Run Contract and Integration Testing</u>*: Run automated contract and API integration test with virtualized integration systems.

- *<u>Regression</u>*: Based on risk score - approach the regression with above checks by product teams and additional regression support by platform QAs if needed.

- *<u>Review biweekly</u>*: Have a biweekly meeting before go live with all QAs to review the impact and test coverage achieved and if there are any.

- *<u>Quarterly release:</u>* full regression of Critical and High areas, end-to-end runs with partner test environments, and UAT with business/POs.

- *<u>Test metrics</u>*: Regularly publishing test metrics- automation %, RCA trends, Defect detection trends (severity/priority), Requirement coverage and **claim accuracy** execution dashboards will get the confidence back and help team keep aligned to achieve the quality targets.

**Summary:** The risk based approach doesn’t mean shifting the focus entirely on the weak areas, it means strategizing the efforts into areas per the situation. Like in this case my **risk based** model would be to move some QA bandwidth from platform team to integration and product with very specific objectives- establish contract testing, API automation and support for kickstarting automation. This along with gradual process improvements I explained above shall address the issues of claim accuracy and integrations.
