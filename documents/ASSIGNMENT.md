Take-Home Exercise: Build a Prototype for ShopSight

Context

We’re exploring new ways to make e-commerce analytics more agentic (search-driven, predictive, and interactive). Imagine a dashboard where a user can search for a product (e.g., “Nike running shoes”) and quickly see:
● Past sales trends (historical data visualization)
● Forecasted demand (e.g., next month’s expected sales)
● Likely customer segments (e.g., who is most likely to buy)
● Other useful insights you think would delight a customer

This is not a full production system—we want a prototype that shows at least one end-to-end flow working while others can be mocked or stubbed out. The goal is to deliver something that could be turned into a customer-facing demo.

Why This Exercise

This assignment is a good representation of the day-to-day work you’d do with us, but on a smaller scope. In our real projects, we often:
● Start from an open-ended problem definition
● Scope down to a small set of high-value features
● Move quickly to a working prototype
● Balance “real” functionality with mocked/stubbed pieces to get a demo in front of users fast
● Integrate LLMs and agentic flows to make analytics more natural and powerful
We’re looking as much at how you approach the problem—your tradeoffs, assumptions, and creativity—as at the final result.

Note: This particular problem doesn’t use Kumo RFM directly. After joining Kumo, you would be building customer-facing solutions powered by Kumo RFM, and also contributing to the Kumo RFM codebase itself to make it easier to use.

The Dataset

We’ve provided a demo dataset here: s3://kumo-public-datasets/hm_with_images/

It contains transactional and item-level data from an e-commerce setting. You may:
● Use this dataset for your working flow(s) (e.g., sales history, product lookup).
● Sample or pre-process it however you like.
● If needed, mock additional data (e.g., forecasts, customer segments) to support your demo.
The Assignment
We expect this to take about 2 hours, since we’re mindful of your time—but this is not a hard limit. Take the time you need to get something working that you’re happy sharing.
Deliverables:
1. A public GitHub repo containing your code.
2. A README.md that explains:
● Your thought process (what you prioritized and why)
● Any assumptions made
● How to run the demo locally
● What’s real vs. what’s mocked
● For any functionality not implemented: describe the gaps and how you would approach building them
3. A few screenshots or a very short video of the demo in action (can be as simple as a screen recording).
Expectations
● At least one core user journey should be functional end-to-end (e.g., product search → past sales chart using the demo data).
● Other features can be mocked with static data or fake APIs, as long as they’re described in the README.
● The solution should leverage an LLM somehow—for example:
● Natural language product search
● Generating human-readable summaries of insights
● Acting as an agent to orchestrate calls to different tools/components
● Tech stack is up to you—choose what lets you move fast.
● Reasonable UX polish is expected given the time, but it doesn’t need to be perfect. The portal should feel navigable and clear.
● This is fairly open-ended — think about what you believe would be most useful and compelling in a customer-facing demo.
Example Directions (Choose Your Own Path)
● Build a simple search box → return a chart of historical sales from the dataset.
● Add an LLM-powered assistant that explains insights in plain English.
● Use an agent pattern to chain together mocked forecast and buyer-segmentation components.
● Show a buyer insights panel that highlights likely users/segments (mocked).
● Implement a “compare items” flow (optional).
Evaluation
We’ll be looking for:
● Clarity of thought in the README
● Ability to scope and prioritize given time constraints
● A working core flow
● How you incorporate LLMs/agentic patterns
● Reasonable UX polish — something demoable and clear, even if not perfect
● Creativity in how you mock or represent missing pieces
● Bonus: thoughtful touches that make it feel customer-ready
⚡️
Note: Don’t worry if it’s incomplete—we want to see how you think, code, and communicate under realistic time constraints.