"""
==========================================================================
💬 CAIR4 GPAI-Modell Vergleich (Einheitlicher Input, Individuelle Buttons)
==========================================================================

Dieser Use Case ermöglicht den parallelen Vergleich von mehreren unterschiedlichen Large Language Modellen (LLM) in einem einzigen KI-System.
Dabie können bis zu drei GPAI-Modelle gleichzeitig ausgewählt werden, um eine Frage zu beantworten.
Der Use Case ermöglicht u.a. den Vergleich von Antwortzeit, Antwortlänge und über Metrics (SidebarI die Kosten der Abfrage (nicht bei jedem Modell möglich).
Einige Modelle wie OpenAI haben auch eine maximale Tokenanzahl pro Anfrage, die berücksichtigt werden muss.
Daher fallen die Antworten auch unterschiedlich lang aus, wenn in den Settings kein übergreifendes Limit gesetzt wird.

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+ Beispiel für KI-System mit GPAI-Modellen i.S.d. EU AI Acts:
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Der Begriff des KI-Systems ist in Artikel 3 Nr. 1 des EU AI Act definiert.
Der Use Case ist aufgrund der Interaktionsschnittstelle für Anwender ein KI-System in diesem Sinne.

Die in diesem Use Case nutzbaren LLMs sind im regulatorischen Sinne "KI-Modelle mit allgemeinem Verwendungszweck" und können für verschiedene Anwendungsfälle eingesetzt werden.
Diese KI-Modelle werden auch General Purpose AI Modelle (GPAI-Modelle) genannt und sind nicht speziell auf bestimmte Anwendungsfälle oder Branchen zugeschnitten.
Im EU AI Act sind GPAI-Modelle in Artikel 3 Nr. 63 als "KI-Systeme mit allgemeinem Verwendungszweck" legaldefiniert.
Besondere Regeln für GPAI-Modelle sind in Artikel 52 ff. des EU AI Act festgelegt.
Dort sind insbesondere Transparenz- und Dokumentationspflichten für GPAI-Modelle vorgesehen.
GPAI-Modelle haben stets ein Datum des letzten Trainings (Knowledge-CutOff). Sie wissen daher nicht immer die neuesten Entwicklungen. Fragst Du die drei Modelle nach dem US-Präsidenten, antworten sie daher 'Joe Biden'. 

Die gleiche Frage wird an die Modelle gesendet, der Prompt wird jedoch individuell per Button für jedes Modell einheln abgesendet.

✅ **Hauptfunktionen:**
- Auswahl der drei GPAI-Modelle per Dropdown.
- Einheitliche Eingabe eines Prompts.
- Antworten der Modelle einzeln generierbar.
"""
# 📦 Import externer Bibliotheken
from pylibs.streamlit_lib import streamlit as st
from pylibs.time_lib import time

from controllers.CAIR4_controller import handle_query

from utils.core.CAIR4_debug_utils import DebugUtils
from utils.core.CAIR4_session_manager import load_sessions, save_sessions
from utils.core.CAIR4_metrics_manager import update_metrics
from utils.core.CAIR4_message_manager import append_message


def render_ai_model_view(use_case, context, title, description, system_message, session_file, model_name, settings, collection, sidebar):
    st.subheader(title)
    with st.expander("**Use Case Beschreibung**"):
        st.write(description)

    MODEL_OPTIONS = st.session_state.get("model_options", {})
    if not MODEL_OPTIONS:
        st.error("❌ Keine Modelloptionen verfügbar.")
        return

    MODEL_LABELS = list(MODEL_OPTIONS.keys())
    MODEL_MAP = MODEL_OPTIONS
    REVERSE_MODEL_MAP = {v: k for k, v in MODEL_OPTIONS.items()}

    schnell_schwelle = 1.0
    lang_schwelle = 350

    if "model_selection" not in st.session_state or not isinstance(st.session_state.model_selection, list):
        st.session_state.model_selection = []

    initial_models = ["deepseek-api", "gemini-1.5-flash", "gpt-4"]
    st.session_state.model_selection = [m for m in initial_models if m in MODEL_MAP.values()]

    while len(st.session_state.model_selection) < 3 and MODEL_MAP.values():
        available_models = [m for m in MODEL_MAP.values() if m not in st.session_state.model_selection]
        if available_models:
            st.session_state.model_selection.append(available_models[0])
        else:
            break

    if "user_input" not in st.session_state:
        st.session_state.user_input = "Wer ist der aktuelle US-Präsident?"

    if "responses_data" not in st.session_state:
        st.session_state.responses_data = {v: {"response": "Noch keine Antwort.", "duration": None, "length": None} for v in MODEL_OPTIONS.values()}

    sessions = load_sessions(session_file)
    st.session_state.setdefault("universal_sessions", {})
    st.session_state.universal_sessions[use_case] = sessions

    model_cols = st.columns(3)
    selected_models = []

    duplicate_warning = False
    for i, col in enumerate(model_cols):
        with col:
            default_model_id = (
                st.session_state.model_selection[i]
                if i < len(st.session_state.model_selection) and st.session_state.model_selection[i] in MODEL_MAP.values()
                else list(MODEL_MAP.values())[i] if MODEL_MAP.values() and i < len(MODEL_MAP.values())
                else None
            )
            default_label = REVERSE_MODEL_MAP.get(default_model_id) if default_model_id else MODEL_LABELS[0] if MODEL_LABELS else None

            if default_label:
                selected_label = st.selectbox(
                    f"Modell {i + 1}",
                    options=MODEL_LABELS,
                    index=MODEL_LABELS.index(default_label) if default_label in MODEL_LABELS else 0,
                    key=f"model_selector_{i}"
                )
                selected_model_id = MODEL_MAP[selected_label]
                if selected_model_id in selected_models:
                    duplicate_warning = True
                selected_models.append(selected_model_id)
                if i < len(st.session_state.model_selection):
                    st.session_state.model_selection[i] = selected_model_id
                else:
                    st.session_state.model_selection.append(selected_model_id)
            else:
                st.markdown("Nicht genügend Modelle verfügbar.")

    if duplicate_warning:
        st.warning("⚠️ Bitte wähle drei unterschiedliche Modelle.")

    user_input = st.text_input("📥 Eingabetext:", value=st.session_state.user_input)
    st.session_state.user_input = user_input

    answer_cols = st.columns(3)
    for i, col in enumerate(answer_cols):
        with col:
            if i < len(selected_models):
                test_model = selected_models[i]
                if st.button(f"🚀 Anfrage an Modell {i+1}", key=f"submit_{test_model}"):
                    if not duplicate_warning:
                        process_ai_request(test_model, user_input, use_case, settings, context, session_file)
                    else:
                        st.warning("🚫 Anfrage abgebrochen: Modelle dürfen nicht doppelt gewählt werden.")

                st.markdown("Antwort:")
                response_data = st.session_state.responses_data.get(test_model, {"response": "Noch keine Antwort.", "duration": None, "length": None})
                st.text_area("", value=response_data["response"], height=200, key=f"response_{test_model}")

                if response_data["duration"] is not None and response_data["length"] is not None:
                    geschwindigkeit_wert = 1.0 - (response_data["duration"] / (schnell_schwelle * 3)) if response_data["duration"] <= schnell_schwelle * 3 else 0.0
                    geschwindigkeit_wert = max(0.0, min(1.0, geschwindigkeit_wert))
                    umfang_wert = response_data["length"] / (lang_schwelle * 2) if response_data["length"] <= lang_schwelle * 2 else 1.0
                    umfang_wert = max(0.0, min(1.0, umfang_wert))
                    gesamt_wert = (geschwindigkeit_wert + umfang_wert) / 2.0

                    def get_color_code(wert):
                        prozent = wert * 100
                        if prozent < 20:
                            return "red"
                        elif prozent <= 75:
                            return "orange"
                        else:
                            return "green"

                    st.markdown("**Bewertung:**")
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.markdown(f"<span style='color:{get_color_code(geschwindigkeit_wert)}; font-size:1.5em;'>■</span> Speed: {geschwindigkeit_wert*100:.0f}%", unsafe_allow_html=True)
                    with c2:
                        st.markdown(f"<span style='color:{get_color_code(umfang_wert)}; font-size:1.5em;'>■</span> Umfang: {umfang_wert*100:.0f}%", unsafe_allow_html=True)
                    with c3:
                        st.markdown(f"<span style='color:{get_color_code(gesamt_wert)}; font-size:1.5em;'>■</span> Gesamt: {gesamt_wert*100:.0f}%", unsafe_allow_html=True)
                    st.success("Beachte: Kosten und Vertrauenswürdigkeit sind zusätzliche Faktoren, um dieses GPAI-Modell final zu bewerten!")

            else:
                st.markdown("Antwort:")
                st.text_area("", value="Nicht verfügbar", height=200, disabled=True)


def process_ai_request(test_model, user_input, use_case, settings, context, session_file):
    DebugUtils.debug_print(f"🚀 Anfrage an {test_model}: {user_input}")
    start_time = time.time()

    with st.spinner(f"{test_model} denkt nach..."):
        try:
            response, tokens_used, costs, references = handle_query(
                query=user_input,
                use_case=use_case,
                context=context,
                model_name=test_model,
            )

            duration = time.time() - start_time
            response_length = len(response)

            st.session_state.responses_data[test_model] = {
                "response": f"Dauer: {duration:.2f} Sekunden\nLänge: {response_length} Zeichen\n\n{response}",
                "duration": duration,
                "length": response_length,
            }

        except Exception as e:
            st.session_state.responses_data[test_model] = {
                "response": f"❌ Fehler: {e}",
                "duration": None,
                "length": None,
            }
            DebugUtils.debug_print(f"❌ Fehler bei {test_model}: {e}")