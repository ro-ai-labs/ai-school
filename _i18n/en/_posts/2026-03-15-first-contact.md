---
layout: article
title: "The First-Contact Protocol"
date: 2026-03-15
author: Mihai Cvasnievschi
reading_time: 10
categories: [ai-literacy]
series: GenAI School
series_order: 2
excerpt_text: "For a year, Maria used ChatGPT to rewrite emails. Then one Tuesday, she stopped asking it to do things for her. She asked it to help her think."
---

For a year, Maria used ChatGPT to rewrite emails.

Maria is a marketing manager at a mid-sized company in Bucharest. If you met her in [the previous article](https://www.linkedin.com/pulse/genai-school-ai-literacy-everybody-gap-mihai-cvasnievschi-icu3f/), you already know the type: sharp, capable, self-taught on AI because nobody else was going to teach her. Subject lines, meeting summaries, the occasional blog outline. She had figured out, through trial and error, how to coax decent results from the machine.

Then one Tuesday, she stopped asking ChatGPT to do things for her. She asked it to help her think. What followed was her First-Contact Protocol.


*This is the second article in the series. New here? Start with [The Gap](https://www.linkedin.com/pulse/genai-school-ai-literacy-everybody-gap-mihai-cvasnievschi-icu3f/), where the story begins.*

### The Question That Changes Everything

Maria did not ask ChatGPT to write anything that Tuesday. She did not ask it to summarise, reformat, or translate. Instead, she tried something different:

> "I am a marketing manager at a mid-sized company in Romania. I work with customer feedback reports, campaign performance data, and product launches. What AI tools should I know about for my role, and how is AI changing marketing right now?"

The response surprised her. Not because it was perfect, but because it was a conversation she had never thought to have. The chatbot mapped out tools she did not know existed. It distinguished between tools she would talk to directly, like ChatGPT itself or Claude, and tools that work silently in the background. Her CRM was scoring leads automatically. Grammarly was rewriting her sentences as she typed. Her email client was suggesting replies she accepted without a second thought.

Then it went further. It described how marketers in similar roles were using AI to cluster customer feedback by sentiment, to spot patterns across campaign data that would take a human analyst days to find, to generate first drafts of competitive analyses from publicly available earnings calls. It outlined workflows she could try this week, not theoretical possibilities from a conference keynote, but practical experiments matched to the tools she already had access to.

For a year, Maria had been using AI to rewrite subject lines. She had been sitting next to a colleague who could help her rethink her entire approach to customer insight, and she had only ever asked it to polish her sentences and tidy her meeting notes.

This is the shift that matters. Not learning a new tool. Not mastering a clever prompt. But discovering that the most powerful AI capability available to you right now is not writing or summarising or generating images. It is conversation. The kind where you bring a genuine question, your actual context, and an open mind, and let the tool help you see what you have been missing.

There is an old observation in business that it is tough to read the label when you are sitting inside the box. You have expertise built over years in your role. But that same expertise can narrow your field of vision. AI does not replace what you know. It offers a vantage point outside the box, a way to see the landscape you have been standing in the middle of.

Of course, Maria could not take the chatbot's landscape map at face value. AI tools can mischaracterise capabilities, invent products that do not exist, or describe features that were discontinued months ago. She would need to verify the suggestions against real sources before trusting any of them. But as a starting point, as a way to generate the right questions rather than supply the final answers, the conversation had already given her more than a year of solo exploration ever had.

*Maria just made her first framework decision without knowing it. She decided this was a task worth using AI for: exploring a landscape too vast to map alone. That instinct, knowing when AI is the right tool for the job, is the first pillar of the SPARKS framework: **SCOPE**.*


### Sharpening the Question

The first answer was broad. Useful, but broad. So Maria followed up:

> "Which of those tools would be most relevant for someone who works mostly with customer feedback data and campaign reporting? And what should I watch out for?"

*Notice what she did. She narrowed the question. Gave context about her actual work. Asked for risks alongside opportunities. Clear, specific instructions that give the AI enough context to be useful: that is **PROMPT**, the second pillar.*

The chatbot refined its answer. It suggested she look at her existing Microsoft 365 Copilot more seriously, particularly its integration with Excel and Word. It flagged that her CRM almost certainly had AI features she had never explored. It mentioned Claude for working with long customer feedback documents. And it warned her: not all of these tools handle data the same way. Some use your inputs for training. Some do not. Some keep data within your organisation's security boundary. Others send it to external servers.

That last point stopped her cold. She had been pasting customer feedback into ChatGPT for months. Not summaries. The raw data. Spreadsheets with customer names, purchase histories, satisfaction scores, complaint details. Last Thursday alone, she had uploaded a file with over two hundred individual records.

She asked, quietly dreading the answer:

> "Where can I find ChatGPT's data usage policy? What should I look for in it?"

The chatbot explained, and she noted the irony of asking a tool to grade its own homework. She would verify later. But the summary was clear enough to act on: the free version of ChatGPT uses conversations for model training by default. Anything she had typed, anything she had uploaded, could in theory influence future outputs seen by other users. There was an opt-out setting, but it was buried in account preferences. She had never touched it.

Two hundred customer names. Months of feedback data. Gone.

She could not retrieve it. She could not undo it. [Samsung's engineers](https://www.bloomberg.com/news/articles/2023-05-02/samsung-bans-chatgpt-and-other-generative-ai-use-by-staff-after-leak) learned the same lesson in April 2023, when three employees pasted source code and meeting transcripts into ChatGPT within weeks of the company lifting its ban. Samsung called the data "impossible to retrieve." [Cyberhaven Labs](https://www.cyberhaven.com/blog/4-2-of-workers-have-pasted-company-data-into-chatgpt) later found that 11% of all data pasted into ChatGPT across 1.6 million workers was classified as confidential. The industry calls it shadow AI, and [IBM's 2025 report](https://www.ibm.com/reports/data-breach) identified it as one of the fastest-growing risk factors in enterprise security.

Maria sat with that for a moment. Then she did what people do when they finally understand a problem: she decided to fix it, properly, starting now. The First-Contact Protocol was no longer an exercise. It was damage control.


### Reading the Fine Print (With Help)

OpenAI's privacy policy was online, a long legal document she would not have read on her own. She opened Claude, one of the tools the chatbot had recommended for working with long documents.

Before uploading, she paused. Was this document safe to share with Claude? A publicly available privacy policy, yes. But she was learning to ask the question first. An internal security audit, a client contract, anything protected by a non-disclosure agreement would not be safe to share with any external tool.

*That pause, weighing what is safe to share before sharing it, is **KEEP-SAFE**.*

With the safety check done, she uploaded the policy and typed:

> "I am evaluating whether ChatGPT is safe to use with client data at work. Based on this document, please answer the following. First, does the tool use my inputs to train or improve its AI models? Second, is my data stored on external servers, and if so, where? Third, can I opt out of data collection, and how? Fourth, who owns the content I create or process with this tool? For each answer, quote the exact passage from the document that supports it."

*Giving the AI a specific document, a clear role, and structured instructions: that is **ARCHITECT**.*

That last instruction, "quote the exact passage," mattered most. In 2023, [a New York lawyer](https://en.wikipedia.org/wiki/Mata_v._Avianca,_Inc.) was fined $5,000 for submitting fabricated legal citations that ChatGPT had generated with complete confidence. AI can misread a document as easily as it can invent a court case. Asking it to cite specific passages gives you something to check against the original. A twenty-page legal document became a five-minute focused review.

*That instinct to verify the AI's work against the source is **REVIEW**.*

The answers confirmed what the chatbot had already told her, but now she could see the exact contractual language. Yes, free-tier conversations were used for training. Yes, she could opt out, through a setting she found and toggled immediately. And the distinction between the free tier and the paid enterprise version was significant.

Next came Microsoft Copilot's documentation. Here, the picture was different. Her company's Microsoft 365 licence meant Copilot conversations stayed within the organisation's security boundary and were not used for model training. She made a note: this is the safe option for anything involving company data. The customer feedback she should have been uploading here all along.

Then the lens turned on Claude itself. It had been her evaluator all evening, but what about its own policies? Anthropic's privacy page revealed that Claude now asks consumer users whether they consent to their conversations being used for training. She had assumed the default was full privacy. It was not. The mental map needed one more adjustment: Claude was a strong research partner for public documents, but not the place for confidential client data on a free account.


### The Silent Tools

The conversation could have stopped there. Three chatbots evaluated, data policies understood, a clear picture of which tool to trust with what.

But then Maria noticed the Grammarly icon pulsing in her browser.

She had been using Grammarly for two years. It rewrote her sentences, suggested tone adjustments, flagged errors. It had read every email she had written, every report she had drafted, every message she had sent to clients. Two years of trust. Not a single question asked.

Not all AI tools have a conversation window where you can type "What is your data policy?" Many of the most consequential AI tools in your working life are the ones you never think to question. Your email client suggests replies. Your CRM scores leads. Your phone transcribes voicemails. Your design software fills in backgrounds. None of these can be interviewed. They simply act.

This is one of the quiet revolutions of our moment. We live in an age where we can ask the tools how to use the other tools.

That evening, Maria found Grammarly's privacy policy on their website and uploaded it into Claude. She used the same prompt, the same four questions. The chatbot parsed the document and extracted the key answers, citing the specific paragraphs that supported each claim. Maria verified the critical ones against the original. Five minutes, and for the first time, she understood what Grammarly had been doing with two years of her professional writing.

The next morning, she went further. She asked Claude about her CRM's AI features:

> "I use [CRM name]. It has AI-powered lead scoring and automated email suggestions. I cannot find clear documentation about how these features work. Can you help me understand what questions I should be asking my IT department, and what settings I should look for?"

The chatbot gave her a checklist: Does the AI process data locally or in the cloud? Can you disable the AI features? Is there an audit log of what the AI has accessed? Are there different data policies for AI features versus core CRM features?

Maria copied the questions and sent them to her IT team. She would get answers within a week. But the point was this: she now knew what to ask. The chatbot had not replaced her judgement. It had equipped her to exercise it.


### What Would You Like Me to Try?

By Wednesday evening, Maria had a clear map. Copilot was the safe choice for client data. Claude and ChatGPT were strong thinking partners, so long as nothing confidential went in. Grammarly and her CRM still needed investigation. Altogether, the conversations had taken less than thirty minutes of actual work, spread across two evenings.

But she wanted one more thing. She went back to ChatGPT and typed:

> "Based on what we have discussed about my role, my tools, and my constraints, what is one concrete experiment I could run this week to test whether AI can genuinely improve my work with customer feedback analysis?"

The chatbot suggested she take her latest quarterly feedback report, upload it to Copilot (the safe option for company data), and ask it to identify the top three customer concerns, compare them to the previous quarter, and flag any patterns that were new. Then compare the AI's analysis against her own. Note where it matched her judgement, where it spotted something she missed, and where it got things wrong.

Maria decided to try it on Thursday. And she would track the results: how long the AI-assisted analysis took compared to her usual manual process, and whether the output was genuinely better or just faster.

*That decision to measure, to compare before and after, to determine whether AI actually helped rather than just produced output that felt productive, is **SCORE**, the sixth and final pillar.*


### The Framework You Just Watched

Maria did not know it, but in under thirty minutes of conversation she had walked through the entire SPARKS framework.

She decided whether to use AI for the task (**SCOPE**). She asked clear, specific questions with enough context to get useful answers (**PROMPT**). She gave the chatbot the right documents and information (**ARCHITECT**). She checked the AI's answers against original sources (**REVIEW**). She made sure nothing confidential leaked into the wrong tool (**KEEP-SAFE**). And she planned a way to measure whether the whole exercise actually helped (**SCORE**).

Six steps. A handful of conversations. No training course, no certification, no two-day workshop.

What Maria just did is the First-Contact Protocol: before you trust any AI tool with real work, sit down with a chatbot and run three conversations. *Help me understand* what AI tools exist for my role. *Help me evaluate* whether each one is safe and capable enough for my work. *Help me plan* a concrete experiment to test whether it actually helps. It is the foundation everything else in this series builds on.

What matters most is this: the protocol does not expire. The tools will change. New models will launch every few months. Features will expand, interfaces will be redesigned, entire products will appear and disappear. But your ability to sit down with a chatbot and use it to map your landscape, evaluate your tools, and plan your next experiment? That is a permanent skill. It works today. It will work on whatever arrives next.

Ethan Mollick of Wharton, whose "jagged frontier" research we explored in [the previous article](https://www.linkedin.com/pulse/genai-school-ai-literacy-everybody-gap-mihai-cvasnievschi-icu3f/), [puts it simply](https://x.com/emollick/status/1671325114141491203): "Today's AI is the worst AI you will ever use." The tools will only get more powerful. The habit of using them as thinking partners, rather than mere task executors, will only grow more important.


### Your Turn

You do not need to wait for a training programme. You have everything you need to run your own First-Contact Protocol right now.

Open ChatGPT, Claude, Gemini, or Copilot. Type a version of Maria's opening question, adapted to your world:

> "I am a [your role] at a [type of company]. I work with [describe your main tasks and data]. What AI tools should I know about, and how is AI changing my profession right now?"

Then follow the conversation wherever it leads. Ask which tools matter most for your specific work. Upload a privacy policy and ask the chatbot to parse it using the four-question prompt Maria used. Ask what experiments you could run this week to test whether AI genuinely helps with your actual tasks.

If you encounter a tool that has no chat interface, a silent AI embedded in software you already use, ask your chatbot to help you evaluate it. Upload the documentation. Ask it to generate the questions you should pose to your IT department. Use the tool that talks to understand the tools that do not.

You are not just learning about AI. You are using AI to learn about AI. And in doing so, you are already practising the framework that the rest of this series will teach.

Incidentally, that habit is also what the law now requires. The [EU AI Act's literacy provisions](https://digital-strategy.ec.europa.eu/en/faqs/ai-literacy-questions-answers) take effect in August 2026, with [member states already standing up enforcement](https://valtioneuvosto.fi/en/-/1410877/national-supervision-of-eu-artificial-intelligence-act-to-begin-laws-on-powers-of-authorities-to-take-effect-at-start-of-the-year). When you run your own First-Contact Protocol, you are building exactly the understanding the Commission expects: what AI is, how it works, which systems you use, and the risks involved. Internal records of such efforts count as evidence of compliance.


### What Comes Next

Maria now knows her tools. She knows which ones to trust, what each one can do, and where the risks live. She also knows, with a clarity that stings, what happens when you skip this step.

But knowing your tools is only the foundation. Once you have mapped your landscape, a harder question follows: should you use AI for this particular task?

Not every task benefits from AI. The Harvard/BCG study from the previous article showed this with painful clarity. When AI was suited to the task, productivity soared. When it was not, experienced professionals performed worse than if they had worked alone. The frontier is jagged, and the penalty for misjudging it is real.

The next article introduces the first pillar of the SPARKS framework: SCOPE. A systematic way to make that go or no-go decision before you write a single prompt. Because the most valuable AI skill is not using the technology well. It is knowing when not to use it at all.


*This is Article 2 of 10 in "GenAI School: AI Literacy for Everybody," a complete, free course on working effectively with AI.*

*Missed the beginning? Start with [The Gap](https://www.linkedin.com/pulse/genai-school-ai-literacy-everybody-gap-mihai-cvasnievschi-icu3f/).*

*Follow for the next article, or share this with someone who needs it.*

*Next: SCOPE*
