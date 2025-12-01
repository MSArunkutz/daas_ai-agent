# DAAS: Disaster Aversion Agentic System

<div align="center">


[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)
[![Gemini](https://img.shields.io/badge/Powered%20by-Gemini%202.5-orange?style=flat-square&logo=google)](https://ai.google.dev/)
[![Phoenix](https://img.shields.io/badge/Observability-Arize%20Phoenix-purple?style=flat-square)](https://phoenix.arize.com/)

**AI-Powered Emergency Response System | Inspired by 2018 Kerala Floods**

![DAAS-Overview](images/DAAS.png)

[Features](#-features) • [Architecture](#-architecture) • [Getting Started](#-getting-started) • [Roadmap](#-roadmap)

</div>

---

## 🌊 The Problem

The **2018 Kerala floods** exposed critical gaps in disaster response:

```
❌ Overwhelmed emergency responders
❌ Confused citizens unsure where to go
❌ Information chaos and misinformation
❌ No 24/7 guidance available
❌ Difficulty coordinating rescue operations
```

**Result**: Countless lives lost, widespread panic, and ineffective resource allocation.

---

## 💡 The Solution

**DAAS** is an AI-powered autonomous agent that provides:

- 🧠 **Context-aware responses** adapted to each emergency situation
- ⏱️ **24/7 availability** without fatigue
- 🎯 **Verified information** from trusted sources only
- 🤝 **Extended reach** for overwhelmed human responders
- 💬 **Empathetic communication** that recognizes urgency and emotion

### Why Autonomous Agents?

Unlike traditional FAQ systems or chatbots, DAAS **understands context** and **adapts dynamically**:

| Traditional Systems | DAAS Agent |
|---------------------|------------|
| Fixed rule-based responses | Context-aware & adaptive |
| One-size-fits-all answers | Personalized guidance |
| Cannot handle nuance | Understands urgency & tone |
| Limited to predefined scenarios | Flexible across situations |

---

## 🌟 Applications Beyond Disasters

DAAS isn't just for floods—it's valuable wherever **large groups need timely, accurate information**:

- 🏟️ **Crowd management** at concerts & public events
- 🎪 **Event coordination** for conferences & festivals  
- 🚨 **Emergency response** for natural disasters
- ❓ **Smart FAQ systems** for complex queries
- 🏥 **Healthcare facilities** for patient guidance

---

## 🏗️ System Architecture
![whatever](images/006%20-%20DAAS%20High%20Level%20Architecture.png)
### Agent Breakdown

```
┌─────────────────────────────────────────────────────────────┐
│                 DAAS_Coordinator (Root Agent)               │
│  Role: Orchestrates flow, routes queries, synthesizes       │
│  LLM: Gemini 2.5 Flash                                      │
└────────────┬──────────────┬─────────────┬───────────────────┘
             │              │             │
    ┌────────▼────────┐ ┌──▼──────────┐ ┌▼─────────────────┐
    │ Flood Intensity │ │ Shelter Aid │ │ get_tips_by_     │
    │     Agent       │ │   Locator   │ │   categories     │
    │                 │ │    Agent    │ │  (Custom Tool)   │
    ├─────────────────┤ ├─────────────┤ ├──────────────────┤
    │ • Flood severity│ │ • Find      │ │ • Safety tips    │
    │   Danger levels │ │   shelters  │ │ • Categorized    │
    │                 │ │   Hospitals │ │   guidance       │
    │                 │ │   5km radius│ │ • Context-aware  │
    └─────────────────┘ └─────────────┘ └──────────────────┘
         Gemini 2.5         Gemini 2.5       Data Filter
         Flash Lite         Flash Lite
```

### Data Flow Diagram

```
User Input
    ↓
[Session Manager] ← In-Memory State
    ↓
[DAAS Coordinator]
    ↓
[Query Classification]
    ↓
┌───────────┬────────────┬───────────┐
│  Flood    │  Location  │   Tips    │
│  Query    │   Query    │   Query   │
└─────┬─────┴──────┬─────┴─────┬─────┘
      ↓            ↓           ↓
 [Agent 1]    [Agent 2]   [Tool 1]
      ↓            ↓           ↓
   [Data]       [Data]      [Data]
      └────────────┴───────────┘
               ↓
      [Response Synthesis]
               ↓
      [Phoenix Logging] ← Observability
               ↓
         User Response
```

---

## ✨ Features

### Core Capabilities

```
┌─────────────────────────────────────────────────────────┐
│                   DAAS Features                         │
├─────────────────────────────────────────────────────────┤
│ ✅ Multi-Agent Coordination                            │
│ ✅ LLM-Powered Intelligence (Gemini 2.5)               │
│ ✅ Flood Severity Assessment                           │
│ ✅ Location-Based Shelter/Hospital Search (5km)        │
│ ✅ Context-Aware Safety Tips                           │
│ ✅ In-Memory Session Management                        │
│ ✅ Full Observability (Arize Phoenix)                  |
│ ✅ Calm & Accurate English Responses                   │
└─────────────────────────────────────────────────────────┘
```

### Technical Stack

| Component | Technology |
|-----------|-----------|
| 🤖 **Language Models** | Google Gemini 2.5 Flash & Flash Lite |
| 🛠️ **Framework** | Google Agent Developer Kit (ADK) |
| 💾 **Session Management** | In-Memory Storage |
| 📊 **Observability** | Arize Phoenix |
| 🐍 **Language** | Python 3.13.9 |
| 📁 **Data** | CSV Files |

---

## 🚀 Getting Started

### Prerequisites

```bash
✓ Python 3.13.9
✓ Google API Key (Gemini)
```

### Quick Installation

```bash
# 1. Clone the repository
git clone https://github.com/MSArunkutz/daas_ai-agent.git
cd daas_ai-agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment
Rename the .env-SAMPLE file to .env and add the GOOGLE_API_KEY

# 4. Run Phoenix first
phoenix serve

# 5. Open another terminal
adk web


```
6. Open browser and follow the address : http://localhost:8000/dev-ui/


### Dataset Disclaimer
This project is inspired by the 2018 Kerala floods. The dataset used here is artificially generated to simulate that scenario. It’s designed to be realistic, but it is not actual disaster data. The geographic scope is limited to Trivandrum city. All place names and shelter names correspond to real locations, but the associated data itself is synthetic.

### Usage Example

```python
# User queries DAAS can handle:

"what is the situation in east fort ?"

→ "Water has entered some streets and ground floors in East Fort, making it unsafe to walk or drive in many areas. Please exercise caution."

"find me shelters near east fort ?"

→ " Here are the nearest shelters within five kilometers of East Fort:

    Arya Samaj Hall Thiruvananthapuram (0.607 km away, 92% capacity)
    University College Thiruvananthapuram (0.727 km away, 95% capacity)
    Town Hall Palayam (0.727 km away, 94% capacity)
    Government Girls HSS Thiruvananthapuram (0.785 km away, 92% capacity)
    Cotton Hill Girls HSS (0.804 km away, 92% capacity)
    Government Model Boys HSS Thiruvananthapuram (1.046 km away, 96% capacity)
    Government Arts College Thiruvananthapuram (1.097 km away, 97% capacity)
    Government Sanskrit College Thiruvananthapuram (1.158 km away, 90% capacity)
    YMCA Hall Thiruvananthapuram (1.158 km away, 94% capacity)
    Tagore Theatre Complex (1.197 km away, 94% capacity)



"What should I do if water is rising?"
→

    Evacuate & Move:
        Move immediately to higher ground.
        Never walk or drive through floodwaters.
        Keep evacuation routes planned and known to your family.
        Follow evacuation orders without delay.
        Keep an emergency bag ready with essential items.
        Assist children, the elderly, and people with disabilities during movement.
        Use only safe and known routes, avoiding shortcuts.
        Avoid traveling at night during heavy rain or flood conditions.
        Wear sturdy shoes and protective clothing.
        Inform your neighbors if you are evacuating and check if they need help.

    Stay Indoors:
        Stay indoors if advised and avoid unnecessary movement.
        Keep windows and doors securely shut and sealed if needed.
        Elevate valuable items to higher levels.
        Monitor water levels from a safe distance while staying inside.
        Ensure your home has enough ventilation for a prolonged stay.
        Stock up on safe drinking water and non-perishable food.
        Use sandbags or barriers to block water from entering your home.
        Avoid using elevators; use stairs if evacuation is needed.
        Keep pets indoors and ensure their safety.
        Stay calm and keep a battery-powered radio to stay informed.

```

---

## 📊 Observability with Phoenix

DAAS uses **Arize Phoenix** for complete system transparency:

### What You Can Monitor

```
┌──────────────────────────────────────────────────┐
│         Phoenix Dashboard Metrics                │
├──────────────────────────────────────────────────┤
│ 📈 Request traces & agent routing               │
│ ⚡ Response times & latency                     │
│ 🎯 Agent performance & accuracy                 │
│ 📊 Query patterns & usage statistics            │
│ 🐛 Error tracking & debugging                   │
│ 🔍 LLM prompt & response quality                │
└──────────────────────────────────────────────────┘
```

**Access Phoenix Dashboard**: (Since phoenix server is already running ) `http://localhost:6006`

---

## 🎯 Agents For Good Track

This project is built for **social impact, not profit**:

### Why DAAS Qualifies

- 🌍 **Pure social welfare** - Free service for all
- ❤️ **Empathetic AI** - Understands emotions, guides calmly
- ⚡ **Always available** - No fatigue, 24/7 support
- 🆓 **Accessible** - Anyone can use during emergencies
- 🚨 **Crisis-focused** - Designed for high-stress situations

### Impact Potential

```
Traditional Response          DAAS-Enhanced Response
─────────────────            ───────────────────────
👥 Limited staff             👥 Staff + AI (unlimited scale)
⏰ Business hours            ⏰ 24/7 availability
📞 Phone queues              💬 Instant responses
📋 Generic advice            🎯 Personalized guidance
😰 Overwhelmed responders    😊 Extended capacity
```

---

## 🔮 Future Vision

![Future Vision](/images/008-%20Future%20Vision.png)

---

## 🧗 My Journey Building This Solo

### Challenges I Overcame

```
🏔️ Steep learning curve → Hands-on practice made it intuitive
🧩 Complex architecture → Breaking into agents simplified it
🤔 Solo decision-making → Learned rapid prototyping & iteration
🐛 Technical hurdles → Phoenix observability helped debug fast
```

### Key Takeaways

- ✅ Agent development becomes **intuitive with practice**
- ✅ Multi-agent systems are **powerful but manageable**
- ✅ Observability tools are **essential for debugging**
- ✅ Solo projects teach **valuable self-reliance skills**

As someone relatively new to AI, I'm proud of what I've built. This is a **prototype with real potential**—and I believe with community support, it can evolve into something that **saves lives**.

---

## 🤝 Contributing
If you'd like to suggest improvements or report issues, feel free to open an issue or pull request.


## 📄 License

Licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

**Inspired by**: The 2018 Kerala floods and the resilience of affected communities

**Powered by**: Google Gemini, Arize Phoenix, and the open-source community

**Dedicated to**: Emergency responders who risk their lives to save others

---

<div align="center">

**Built with ❤️ for social good**

*"In disasters, every second counts. DAAS ensures help is always available."*

---

**Arun Kutz MS** | [GitHub](https://github.com/MSArunkutz) | [Project Repository](https://github.com/MSArunkutz/daas_ai-agent)

---

⭐ **Star this project if you believe in using AI for social good!** ⭐

</div>