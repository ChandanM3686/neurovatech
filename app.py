import os
import streamlit as st
from retell import Retell, APIStatusError
import streamlit.components.v1 as components

st.set_page_config(
    page_title="AI Voice Agent",
    layout="wide",
    page_icon="🎙️",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.2rem;
        font-weight: 800;
        margin-bottom: 0.75rem;
    }
    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 1.05rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    .agent-grid {
        margin-top: 0.5rem;
    }
    .agent-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid #e9ecef;
        box-shadow: 0 8px 26px rgba(0, 0, 0, 0.06);
        transition: transform .25s ease, box-shadow .25s ease;
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    .agent-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 44px rgba(0, 0, 0, 0.10);
    }
    .agent-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    .agent-icon {
        font-size: 2.4rem;
        text-align: center;
        margin-bottom: 0.75rem;
        display: block;
    }
    .agent-title {
        font-size: 1.25rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: .5rem;
        color: #111827;
    }
    .agent-description {
        text-align: center;
        color: #6b7280;
        margin-bottom: 1rem;
        line-height: 1.5;
        font-size: .95rem;
        min-height: 48px;
    }
    .agent-features {
        background: #f8fafc;
        border-radius: 12px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.75rem;
        border: 1px solid #eef2f7;
    }
    .agent-features ul {
        margin: 0;
        padding-left: 1.2rem;
        color: #495057;
        font-size: .92rem;
    }
    .agent-features li {
        margin-bottom: 0.35rem;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 999px;
        padding: 0.6rem 1.2rem;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.25s ease;
        width: 100%;
        box-shadow: 0 6px 18px rgba(102, 126, 234, 0.35);
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 26px rgba(102, 126, 234, 0.45);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    .status-success {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem 1.25rem;
        border-radius: 14px;
        margin: 1rem 0 0.5rem;
        box-shadow: 0 5px 15px rgba(21, 87, 36, 0.08);
    }
    .status-error {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem 1.25rem;
        border-radius: 14px;
        margin: 1rem 0 0.5rem;
        box-shadow: 0 5px 15px rgba(114, 28, 36, 0.08);
    }
    .metrics-container {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1rem 1.25rem;
        border-radius: 14px;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.06);
        margin: 0.75rem 0;
        border: 1px solid #eef2f7;
    }
    .voice-interface {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.25rem;
        border-radius: 18px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        margin: 1rem 0 0.5rem;
        border: 1px solid #eef2f7;
    }
    .instructions-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 1rem 1.25rem;
        border-radius: 14px;
        margin: 0.5rem 0 1rem;
        border-left: 5px solid #2196f3;
    }
</style>
""", unsafe_allow_html=True)

# ------------- Retell init + Settings -------------
def _get_retell_api_key() -> str:
    env_key = os.getenv("RETELL_API_KEY")
    if env_key:
        return env_key
    try:
        return st.secrets["RETELL_API_KEY"]
    except Exception:
        # Built-in default key (requested to be hardcoded)
        return "key_c4c91d9723a5cdeb2c14f9b18919"

if "agents_override" not in st.session_state:
    st.session_state.agents_override = {}

def get_retell_client() -> Retell:
    return Retell(api_key=_get_retell_api_key())

# ------------- Agents (merged: your Flask + Dental) -------------
AGENTS = {
    # From your Flask app
    "real_estate": "agent_47bcafb59b39c5e0a488edf4d9",
    "debits": "agent_b1329cafcfb061e2bad5e7ee6f",
    "insurance": "agent_49db8c2060bf33531273213e05",
    "healthcare": "agent_cdd1db6ff8c3fcbbb7e624d82f",
    "school": "agent_42244218fe2434b394823229f3",
    "ecommerce": "agent_6f60a841012f3b6caa758cced7",
    "travel": "agent_90bbd9f42b1e8991c6354f2d18",
    "fintech": "agent_c3d2c3598247fc9c9f876a842c",
    "utility": "agent_ae0cbbbc5847928a53c9fc7ca3",
    "restaurant": "agent_085d0c296fb0aa4c4623faff24",
    # From your Streamlit snippet
    "dental": "agent_4deac7a40e9e59967e58066b88",
}

# ------------- Helpers -------------
def get_effective_agent_id(agent_key: str) -> str:
    # Priority: sidebar override -> env var -> built-in default
    if agent_key in st.session_state.agents_override:
        return st.session_state.agents_override[agent_key]
    env_val = os.getenv(f"RETELL_AGENT_{agent_key.upper()}")
    if env_val:
        return env_val
    return AGENTS.get(agent_key, "")

# ------------- Agent metadata for UI -------------
AGENT_INFO = {
    "real_estate": {
        "icon": "🏡",
        "title": "Real Estate Assistant",
        "description": "Property search, scheduling tours, mortgage basics, and neighborhood insights.",
        "features": [
            "Find properties by budget & location",
            "Schedule viewings and callbacks",
            "Mortgage & financing basics",
            "Neighborhood & school info",
            "Offer & closing guidance",
        ],
    },
    "debits": {
        "icon": "🏦",
        "title": "Debits Assistant",
        "description": "Billing, payment support, and account adjustments with secure verification.",
        "features": [
            "Explain charges & statements",
            "Update or pause payments",
            "Set up autopay & reminders",
            "Refund & dispute guidance",
            "Secure identity verification",
        ],
    },
    "insurance": {
        "icon": "🛡️",
        "title": "Insurance Assistant",
        "description": "Policy explanations, quotes, and claims status across multiple lines.",
        "features": [
            "Auto/Home/Health/Life quotes",
            "Coverage & deductible info",
            "File & track claims",
            "Find in-network providers",
            "Renewal reminders",
        ],
    },
    "healthcare": {
        "icon": "🏥",
        "title": "Healthcare Assistant",
        "description": "Appointment booking, provider lookup, and pre-visit instructions.",
        "features": [
            "Book & reschedule appointments",
            "Check insurance acceptance",
            "Provider availability",
            "Pre-visit preparation",
            "Follow-up reminders",
        ],
    },
    "school": {
        "icon": "🎓",
        "title": "School Assistant",
        "description": "Admissions help, course info, schedule & event reminders.",
        "features": [
            "Admissions & deadlines",
            "Course & curriculum info",
            "Campus tour scheduling",
            "Event & exam reminders",
            "Financial aid basics",
        ],
    },
    "ecommerce": {
        "icon": "🛒",
        "title": "E-commerce Assistant",
        "description": "Order status, returns, recommendations, and support.",
        "features": [
            "Track order & delivery",
            "Returns & exchanges",
            "Product Q&A",
            "Personalized recommendations",
            "Promo & stock updates",
        ],
    },
    "travel": {
        "icon": "✈️",
        "title": "Travel Assistant",
        "description": "Flights, hotels, itinerary changes, and local tips.",
        "features": [
            "Book flights & hotels",
            "Change or cancel trips",
            "Visa & baggage info",
            "Local transport tips",
            "Real-time alerts",
        ],
    },
    "fintech": {
        "icon": "💳",
        "title": "Fintech Assistant",
        "description": "Account support, transfers, security, and insights.",
        "features": [
            "Balance & transaction info",
            "Transfers & bill pay",
            "Card lock/unlock",
            "Fraud alerts & security",
            "Spending insights",
        ],
    },
    "utility": {
        "icon": "⚡",
        "title": "Utility Assistant",
        "description": "Outages, billing, usage, and service appointments.",
        "features": [
            "Report & track outages",
            "Billing & autopay",
            "Usage analytics",
            "Move-in/move-out service",
            "Technician scheduling",
        ],
    },
    "restaurant": {
        "icon": "🍽️",
        "title": "Restaurant Assistant",
        "description": "Reservations, menu guidance, dietary info, and special occasions.",
        "features": [
            "Make & modify reservations",
            "Menu recommendations",
            "Allergy & dietary support",
            "Wait time & seating info",
            "Event & group planning",
        ],
    },
    "dental": {
        "icon": "🦷",
        "title": "Dental Assistant",
        "description": "Scheduling, procedure info, and oral health guidance.",
        "features": [
            "Book dental appointments",
            "Procedure explanations",
            "Insurance & coverage basics",
            "Post-op care guidance",
            "Emergency triage tips",
        ],
    },
}

# ------------- Sidebar: Settings (agent IDs only) -------------
with st.sidebar:
    st.subheader("Settings")
    with st.expander("Configure Agent IDs", expanded=False):
        for _agent_key, meta in AGENT_INFO.items():
            env_override = os.getenv(f"RETELL_AGENT_{_agent_key.upper()}", "")
            default_val = (
                st.session_state.agents_override.get(_agent_key)
                or env_override
                or AGENTS.get(_agent_key, "")
            )
            st.text_input(
                f"{meta['title']} ID",
                value=default_val,
                key=f"cfg_agent_id__{_agent_key}",
                help=f"Set Retell agent id for {_agent_key} (e.g., agent_xxx)",
            )

    if st.button("Apply settings", type="primary", use_container_width=True):
        overrides: dict[str, str] = {}
        for _agent_key in AGENT_INFO.keys():
            v = (st.session_state.get(f"cfg_agent_id__{_agent_key}", "") or "").strip()
            if v:
                overrides[_agent_key] = v
        st.session_state.agents_override = overrides
        st.success("Settings applied.")

# ------------- Session State -------------
if "selected_agent" not in st.session_state:
    st.session_state.selected_agent = None
if "call_active" not in st.session_state:
    st.session_state.call_active = False

# ------------- Header -------------
st.markdown('<h1 class="main-header">🎙️  AI Voice Agents</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Choose a specialized assistant and start a real-time voice conversation</p>', unsafe_allow_html=True)

# ------------- Agent Cards Grid -------------
def render_agent_card(agent_key: str):
    info = AGENT_INFO[agent_key]
    features_html = ''.join([f'<li>{f}</li>' for f in info["features"]])
    st.markdown(f"""
    <div class="agent-card">
        <div class="agent-icon">{info['icon']}</div>
        <div class="agent-title">{info['title']}</div>
        <div class="agent-description">{info['description']}</div>
        <div class="agent-features">
            <strong>🌟 Key Features:</strong>
            <ul>{features_html}</ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    return st.button(f"🎙️ Start {info['title']}", key=f"btn_{agent_key}", help=f"Begin conversation with {info['title']}")

# Render in rows of N columns
COLS = 3
agent_keys = list(AGENT_INFO.keys())
rows = (len(agent_keys) + COLS - 1) // COLS

with st.container():
    st.markdown('<div class="agent-grid">', unsafe_allow_html=True)
    idx = 0
    for _ in range(rows):
        cols = st.columns(COLS, gap="large")
        for c in cols:
            if idx < len(agent_keys):
                key = agent_keys[idx]
                with c:
                    if render_agent_card(key):
                        st.session_state.selected_agent = key
                        st.session_state.call_active = True
                idx += 1
    st.markdown('</div>', unsafe_allow_html=True)

# ------------- Voice Call Flow -------------
if st.session_state.call_active and st.session_state.selected_agent:
    agent_key = st.session_state.selected_agent
    info = AGENT_INFO[agent_key]

    st.markdown("---")
    st.markdown(f"### 🚀 Initializing {info['title']}")

    with st.spinner(f"🔄 Setting up your {info['title']} voice session..."):
        try:
            # Ensure API key configured before attempting network call
            if not _get_retell_api_key():
                raise RuntimeError(
                    "No Retell API key configured. The code expects a hardcoded key in _get_retell_api_key()."
                )
            # Rebuild client with the latest key from settings
            client = get_retell_client()

            # Compute effective agent id (supports overrides)
            agent_id = get_effective_agent_id(agent_key)
            if not agent_id:
                raise RuntimeError(f"No agent id configured for '{agent_key}'. Configure it in the sidebar settings.")

            response = client.call.create_web_call(agent_id=agent_id)
            data = response.to_dict()

            st.markdown(f"""
            <div class="status-success">
                <h4>✅ {info['title']} Ready</h4>
                <p>Your AI assistant is now active. The voice interface will appear below.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
            st.markdown("#### 📊 Session Information")
            col_info1, col_info2, col_info3, col_info4 = st.columns(4)
            with col_info1:
                st.metric("🤖 Agent", info["title"])
            with col_info2:
                st.metric("📞 Call ID", (data.get("call_id", "N/A") or "N/A")[:8] + "...")
            with col_info3:
                st.metric("🟢 Status", "Active")
            with col_info4:
                st.metric("🎵 Quality", "24kHz HD")
            st.markdown('</div>', unsafe_allow_html=True)

            with st.expander("🔧 Technical Details", expanded=False):
                st.json(data)

            access_token = data.get("access_token")

            if access_token:
                st.markdown('<div class="voice-interface">', unsafe_allow_html=True)
                st.markdown("### 🎧 Voice Interface")
                st.markdown(f"""
                <div class="instructions-box">
                    <h4>📢 How to interact with your {info['title']}:</h4>
                    <ul>
                        <li><strong>🎤 Allow microphone access</strong> when prompted</li>
                        <li><strong>🗣️ Speak naturally</strong> – no special commands needed</li>
                        <li><strong>👂 Listen to voice replies</strong> in real-time</li>
                        <li><strong>📝 Watch the transcript</strong> update below</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

                components.html(f"""
                <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 20px; background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
                    <div id="status" style="padding: 12px; margin-bottom: 16px; background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); border-radius: 12px; border-left: 5px solid #f39c12; box-shadow: 0 5px 15px rgba(243,156,18,0.2);">
                        <strong style="font-size: 1rem;">🔄 Initializing {info['title']} voice client...</strong>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 220px; gap: 16px; margin-bottom: 12px;">
                        <div id="transcript-container" style="background: white; padding: 16px; border-radius: 12px; min-height: 280px; border: 1px solid #dee2e6; box-shadow: 0 5px 15px rgba(0,0,0,0.05);">
                            <h4 style="margin-top: 0; color: #374151; display: flex; align-items: center; gap: 8px;">
                                <span style="font-size: 1.4rem;">📝</span> Live Conversation
                            </h4>
                            <div id="transcript" style="font-family: 'Courier New', monospace; color: #6b7280; line-height: 1.55;">
                                <div style="text-align: center; padding: 36px; color: #9ca3af;">
                                    <div style="font-size: 2.4rem; margin-bottom: 8px;">{info['icon']}</div>
                                    <p>Waiting for conversation to begin...</p>
                                </div>
                            </div>
                        </div>

                        <div style="display: flex; flex-direction: column; gap: 12px;">
                            <div id="voice-status" style="background: white; padding: 14px; border-radius: 12px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.05);">
                                <div style="font-size: 1.8rem; margin-bottom: 8px;">🎤</div>
                                <div style="font-size: 0.9rem; color: #6b7280;">Voice Status</div>
                                <div id="voice-indicator" style="font-weight: 800; color: #28a745;">Initializing</div>
                            </div>

                            <div style="background: white; padding: 14px; border-radius: 12px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.05);">
                                <div style="font-size: 1.8rem; margin-bottom: 8px;">⏱️</div>
                                <div style="font-size: 0.9rem; color: #6b7280;">Session Time</div>
                                <div id="session-timer" style="font-weight: 800; color: #2563eb;">00:00</div>
                            </div>

                            <div style="background: white; padding: 14px; border-radius: 12px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.05);">
                                <div style="font-size: 1.8rem; margin-bottom: 8px;">💬</div>
                                <div style="font-size: 0.9rem; color: #6b7280;">Messages</div>
                                <div id="message-count" style="font-weight: 800; color: #6f42c1;">0</div>
                            </div>
                        </div>
                    </div>
                </div>

                <script type="module">
                    import {{ RetellWebClient }} from 'https://cdn.jsdelivr.net/npm/retell-client-js-sdk/+esm';

                    const statusDiv = document.getElementById('status');
                    const transcriptDiv = document.getElementById('transcript');
                    const voiceIndicator = document.getElementById('voice-indicator');
                    const sessionTimer = document.getElementById('session-timer');
                    const messageCount = document.getElementById('message-count');

                    let startTime = Date.now();
                    let messageCounter = 0;

                    setInterval(() => {{
                        const elapsed = Math.floor((Date.now() - startTime) / 1000);
                        const minutes = Math.floor(elapsed / 60);
                        const seconds = elapsed % 60;
                        sessionTimer.textContent = `${{minutes.toString().padStart(2, '0')}}:${{seconds.toString().padStart(2, '0')}}`;
                    }}, 1000);

                    function updateStatus(message, type = 'info') {{
                        const styles = {{
                            'success': 'background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); border-left-color: #28a745;',
                            'error': 'background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%); border-left-color: #dc3545;',
                            'info': 'background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%); border-left-color: #17a2b8;',
                            'warning': 'background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); border-left-color: #f39c12;'
                        }};
                        statusDiv.style.cssText = styles[type] + 'padding: 12px; margin-bottom: 16px; border-radius: 12px; border-left: 5px solid; box-shadow: 0 5px 15px rgba(0,0,0,0.08);';
                        statusDiv.innerHTML = `<strong style="font-size: 1rem;">${{message}}</strong>`;
                    }}

                    function addTranscript(text, speaker = 'user') {{
                        const timestamp = new Date().toLocaleTimeString();
                        const speakerIcon = speaker === 'agent' ? '{info['icon']}' : '👤';
                        const speakerColor = speaker === 'agent' ? '#2563eb' : '#059669';
                        const bgColor = speaker === 'agent' ? '#eef5ff' : '#ecfdf5';

                        if (transcriptDiv.innerHTML.includes('Waiting for conversation')) {{
                            transcriptDiv.innerHTML = '';
                        }}

                        transcriptDiv.innerHTML += `
                            <div style="margin: 10px 0; padding: 12px; border-left: 4px solid ${{speakerColor}}; background: ${{bgColor}}; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                                    <strong style="color: ${{speakerColor}}; display: flex; align-items: center; gap: 8px;">
                                        <span style="font-size: 1.1rem;">${{speakerIcon}}</span>
                                        ${{speaker.charAt(0).toUpperCase() + speaker.slice(1)}}
                                    </strong>
                                    <small style="color: #6b7280; font-size: 0.78rem;">${{timestamp}}</small>
                                </div>
                                <div style="color: #374151; line-height: 1.5;">${{text}}</div>
                            </div>
                        `;
                        transcriptDiv.scrollTop = transcriptDiv.scrollHeight;

                        messageCounter++;
                        messageCount.textContent = messageCounter;
                    }}

                    try {{
                        const client = new RetellWebClient();

                        updateStatus('🎙️ Connecting to {info['title']}...', 'info');
                        voiceIndicator.textContent = 'Connecting';
                        voiceIndicator.style.color = '#f59e0b';

                        await client.startCall({{
                            accessToken: "{access_token}",
                            sampleRate: 24000
                        }});

                        updateStatus('✅ {info['title']} is ready! Start speaking...', 'success');
                        voiceIndicator.textContent = 'Ready';
                        voiceIndicator.style.color = '#10b981';

                        transcriptDiv.innerHTML = `
                            <div style="text-align: center; padding: 24px; background: linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%); border-radius: 12px; margin-bottom: 12px;">
                                <div style="font-size: 2.4rem; margin-bottom: 8px;">{info['icon']}</div>
                                <h3 style="color: #059669; margin: 0 0 6px;">🎉 {info['title']} Active!</h3>
                                <p style="color: #155724; margin: 0;">Your conversation will appear here in real-time</p>
                            </div>
                        `;

                        client.on('update', (update) => {{
                            if (update.transcript) {{
                                addTranscript(update.transcript, 'user');
                            }}
                        }});

                        client.on('agent_start_talking', () => {{
                            updateStatus('🤖 {info['title']} is speaking...', 'info');
                            voiceIndicator.textContent = 'AI Speaking';
                            voiceIndicator.style.color = '#2563eb';
                        }});

                        client.on('agent_stop_talking', () => {{
                            updateStatus('👂 Listening for your response...', 'success');
                            voiceIndicator.textContent = 'Listening';
                            voiceIndicator.style.color = '#10b981';
                        }});

                        client.on('call_ended', () => {{
                            updateStatus('📞 Conversation ended - Thank you!', 'warning');
                            voiceIndicator.textContent = 'Ended';
                            voiceIndicator.style.color = '#6b7280';
                        }});
                    }} catch (err) {{
                        updateStatus(`❌ Connection failed: ${{err.message}}`, 'error');
                        voiceIndicator.textContent = 'Error';
                        voiceIndicator.style.color = '#dc3545';
                        console.error('Call error:', err);
                    }}
                </script>
                """, height=650)

                st.markdown('</div>', unsafe_allow_html=True)

                # Reset
                if st.button("🔄 Start New Conversation", help="Reset and choose a different agent"):
                    st.session_state.selected_agent = None
                    st.session_state.call_active = False
                    st.rerun()
            else:
                st.markdown("""
                <div class="status-error">
                    <h4>❌ Access Token Missing</h4>
                    <p>No access token received from the API. Cannot initiate the voice call.</p>
                </div>
                """, unsafe_allow_html=True)

        except APIStatusError as e:
            st.markdown(f"""
            <div class="status-error">
                <h4>🚫 Retell API Error</h4>
                <p><strong>Status Code:</strong> {getattr(e, 'status_code', 'N/A')}</p>
                <p><strong>Error Details:</strong> {e.get_body_text() if hasattr(e, 'get_body_text') else str(e)}</p>
                <p><em>Please try again or contact support if the issue persists.</em></p>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            # Provide clearer guidance on common connectivity issues
            msg = str(e)
            hint = ""
            lower = msg.lower()
            if "connect" in lower or "connection" in lower or "dns" in lower or "timeout" in lower:
                hint = (
                    "Check your internet connection, VPN/proxy settings, and ensure the API key is valid. "
                    "If you're behind a corporate proxy, configure HTTPS_PROXY/HTTP_PROXY environment variables."
                )
            elif "api key" in lower or "unauthorized" in lower or "401" in lower:
                hint = "Your API key may be missing or invalid. Set a valid key in the sidebar and apply."
            st.markdown(f"""
            <div class="status-error">
                <h4>⚠️ Unexpected Error</h4>
                <p><strong>Error:</strong> {msg}</p>
                {f'<p><em>{hint}</em></p>' if hint else ''}
            </div>
            """, unsafe_allow_html=True)

# ------------- Footer -------------
if not st.session_state.call_active:
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 1.25rem; padding: 1.25rem; background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 16px;">
        <h4 style="color: #374151; margin-bottom: 0.5rem;">🔒 Privacy & Security</h4>
        <p style="margin-bottom: 0.5rem;">Your conversations are secure, encrypted, and never stored permanently</p>
        <div style="display: flex; justify-content: center; gap: 1.25rem; flex-wrap: wrap; margin-top: 0.75rem; font-size: .95rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span>🛡️</span>
                <span>End-to-End Encrypted</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span>🚀</span>
                <span>Powered by AI</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span>⚡</span>
                <span>Built with Streamlit</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)