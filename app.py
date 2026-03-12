# # """
# # Career Intelligence Assistant - Streamlit Application
# # A conversational AI assistant for career fit assessment and interview preparation.
# # """

# # import streamlit as st
# # import os
# # from typing import Dict, List
# # from utils.document_parser import DocumentParser
# # from utils.llm_helper import CareerIntelligenceAssistant
# # from dotenv import load_dotenv
# # load_dotenv()


# # # Page configuration
# # st.set_page_config(
# #     page_title="Career Intelligence Assistant",
# #     page_icon="🎯",
# #     layout="wide",
# #     initial_sidebar_state="expanded"
# # )

# # # Custom CSS for better UI
# # st.markdown("""
# #     <style>
# #     .main-header {
# #         font-size: 2.5rem;
# #         font-weight: bold;
# #         color: #1E88E5;
# #         text-align: center;
# #         padding: 1rem 0;
# #     }
# #     .sub-header {
# #         font-size: 1.2rem;
# #         color: #666;
# #         text-align: center;
# #         margin-bottom: 2rem;
# #     }
# #     .file-info {
# #         background-color: #f0f2f6;
# #         padding: 1rem;
# #         border-radius: 0.5rem;
# #         margin: 0.5rem 0;
# #     }
# #     .chat-message {
# #         padding: 1rem;
# #         border-radius: 0.5rem;
# #         margin: 0.5rem 0;
# #     }
# #     .user-message {
# #         background-color: #e3f2fd;
# #     }
# #     .assistant-message {
# #         background-color: #f5f5f5;
# #     }
# #     .stButton>button {
# #         width: 100%;
# #     }
# #     </style>
# # """, unsafe_allow_html=True)


# # def initialize_session_state():
# #     """Initialize session state variables."""
# #     if 'resume_text' not in st.session_state:
# #         st.session_state.resume_text = None
# #     if 'resume_filename' not in st.session_state:
# #         st.session_state.resume_filename = None
# #     if 'job_postings' not in st.session_state:
# #         st.session_state.job_postings = {}  # {job_number: {"name": str, "content": str}}
# #     if 'conversation_history' not in st.session_state:
# #         st.session_state.conversation_history = []
# #     if 'assistant' not in st.session_state:
# #         try:
# #             api_key = os.getenv('OPENAI_API_KEY')
# #             if api_key:
# #                 st.session_state.assistant = CareerIntelligenceAssistant(api_key=api_key)
# #             else:
# #                 st.session_state.assistant = None
# #         except:
# #             st.session_state.assistant = None
# #     if 'job_counter' not in st.session_state:
# #         st.session_state.job_counter = 0


# # def parse_uploaded_file(uploaded_file):
# #     """Parse uploaded file and extract text.
    
# #     Args:
# #         uploaded_file: Streamlit UploadedFile object
        
# #     Returns:
# #         Extracted text content
# #     """
# #     try:
# #         file_bytes = uploaded_file.read()
# #         text = DocumentParser.parse_file(file_bytes, uploaded_file.name)
# #         return text
# #     except Exception as e:
# #         st.error(f"Error parsing {uploaded_file.name}: {str(e)}")
# #         return None


# # def display_uploaded_files():
# #     """Display information about uploaded files."""
# #     st.markdown("### 📄 Uploaded Documents")
    
# #     col1, col2 = st.columns(2)
    
# #     with col1:
# #         st.markdown("**Resume:**")
# #         if st.session_state.resume_filename:
# #             st.markdown(f"✅ {st.session_state.resume_filename}")
# #         else:
# #             st.markdown("❌ No resume uploaded")
    
# #     with col2:
# #         st.markdown("**Job Postings:**")
# #         if st.session_state.job_postings:
# #             for job_num, job_data in st.session_state.job_postings.items():
# #                 st.markdown(f"✅ Job #{job_num}: {job_data['name']}")
# #         else:
# #             st.markdown("❌ No job postings uploaded")
    
# #     st.markdown("---")


# # def display_chat_interface():
# #     """Display the chat interface with conversation history."""
# #     st.markdown("### 💬 Ask Questions")
    
# #     # Display conversation history
# #     for message in st.session_state.conversation_history:
# #         if message["role"] == "user":
# #             st.markdown(f"""
# #                 <div class="chat-message user-message">
# #                     <strong>You:</strong> {message["content"]}
# #                 </div>
# #             """, unsafe_allow_html=True)
# #         else:
# #             st.markdown(f"""
# #                 <div class="chat-message assistant-message">
# #                     <strong>Assistant:</strong> {message["content"]}
# #                 </div>
# #             """, unsafe_allow_html=True)
    
# #     # Chat input
# #     user_input = st.chat_input("Ask about your career fit, skills gaps, interview prep, etc.")
    
# #     if user_input:
# #         handle_user_message(user_input)


# # def handle_user_message(user_message: str):
# #     """Handle user message and get response from assistant.
    
# #     Args:
# #         user_message: User's input message
# #     """
# #     # Check if resume is uploaded
# #     if not st.session_state.resume_text:
# #         st.error("⚠️ Please upload your resume first!")
# #         return
    
# #     # Check if assistant is initialized
# #     if not st.session_state.assistant:
# #         st.error("⚠️ Please configure your OpenAI API key!")
# #         return
    
# #     # Add user message to history
# #     st.session_state.conversation_history.append({
# #         "role": "user",
# #         "content": user_message
# #     })
    
# #     # Get response from assistant
# #     with st.spinner("Thinking..."):
# #         response = st.session_state.assistant.get_response(
# #             resume=st.session_state.resume_text,
# #             job_postings=st.session_state.job_postings,
# #             conversation_history=st.session_state.conversation_history[:-1],  # Exclude current message
# #             user_message=user_message
# #         )
    
# #     # Add assistant response to history
# #     st.session_state.conversation_history.append({
# #         "role": "assistant",
# #         "content": response
# #     })
    
# #     # Rerun to update the display
# #     st.rerun()


# # def sidebar_config():
# #     """Configure sidebar with file uploads and settings."""
# #     st.sidebar.markdown("## 🎯 Career Intelligence Assistant")
# #     st.sidebar.markdown("Upload your resume and job postings to get started!")
# #     st.sidebar.markdown("---")
    
# #     # API Key Configuration
# #     st.sidebar.markdown("### 🔑 API Configuration")
# #     api_key = st.sidebar.text_input(
# #         "OpenAI API Key",
# #         value=os.getenv('OPENAI_API_KEY', ''),
# #         type="password",
# #         help="Enter your OpenAI API key"
# #     )
    
# #     if api_key:
# #         os.environ['OPENAI_API_KEY'] = api_key
# #         if not st.session_state.assistant:
# #             try:
# #                 st.session_state.assistant = CareerIntelligenceAssistant(api_key=api_key)
# #                 st.sidebar.success("✅ API key configured!")
# #             except Exception as e:
# #                 st.sidebar.error(f"❌ Error: {str(e)}")
# #     else:
# #         st.sidebar.warning("⚠️ API key required for AI features")
    
# #     st.sidebar.markdown("---")
    
# #     # Resume Upload
# #     st.sidebar.markdown("### 📄 Upload Resume")
# #     resume_file = st.sidebar.file_uploader(
# #         "Upload your resume",
# #         type=['pdf', 'docx', 'txt'],
# #         key="resume_uploader",
# #         help="Supported formats: PDF, DOCX, TXT"
# #     )
    
# #     if resume_file:
# #         if st.sidebar.button("Parse Resume", key="parse_resume"):
# #             with st.spinner("Parsing resume..."):
# #                 resume_text = parse_uploaded_file(resume_file)
# #                 if resume_text:
# #                     st.session_state.resume_text = resume_text
# #                     st.session_state.resume_filename = resume_file.name
# #                     st.sidebar.success(f"✅ Resume parsed: {resume_file.name}")
# #                     st.rerun()
    
# #     st.sidebar.markdown("---")
    
# #     # Job Postings Upload
# #     st.sidebar.markdown("### 📋 Upload Job Postings")
# #     job_files = st.sidebar.file_uploader(
# #         "Upload job postings (multiple files)",
# #         type=['pdf', 'docx', 'txt'],
# #         accept_multiple_files=True,
# #         key="job_uploader",
# #         help="Upload one or more job postings"
# #     )
    
# #     if job_files:
# #         if st.sidebar.button("Parse Job Postings", key="parse_jobs"):
# #             with st.spinner("Parsing job postings..."):
# #                 for job_file in job_files:
# #                     job_text = parse_uploaded_file(job_file)
# #                     if job_text:
# #                         st.session_state.job_counter += 1
# #                         st.session_state.job_postings[st.session_state.job_counter] = {
# #                             "name": job_file.name,
# #                             "content": job_text
# #                         }
# #                         st.sidebar.success(f"✅ Parsed: {job_file.name}")
# #                 st.rerun()
    
# #     st.sidebar.markdown("---")
    
# #     # Clear Data
# #     st.sidebar.markdown("### 🗑️ Clear Data")
# #     col1, col2 = st.sidebar.columns(2)
    
# #     with col1:
# #         if st.button("Clear Chat", key="clear_chat"):
# #             st.session_state.conversation_history = []
# #             st.rerun()
    
# #     with col2:
# #         if st.button("Clear All", key="clear_all"):
# #             st.session_state.resume_text = None
# #             st.session_state.resume_filename = None
# #             st.session_state.job_postings = {}
# #             st.session_state.conversation_history = []
# #             st.session_state.job_counter = 0
# #             st.rerun()
    
# #     st.sidebar.markdown("---")
    
# #     # Example Questions
# #     st.sidebar.markdown("### 💡 Example Questions")
# #     st.sidebar.markdown("""
# #     - What skills am I missing for Job #1?
# #     - How does my experience align with Job #2?
# #     - What are my strengths for this role?
# #     - Help me prepare for an interview
# #     - What should I emphasize in my cover letter?
# #     - Which job posting is the best fit for me?
# #     """)


# # def main_content():
# #     """Display main content area."""
# #     # Header
# #     st.markdown('<div class="main-header">🎯 Career Intelligence Assistant</div>', unsafe_allow_html=True)
# #     st.markdown('<div class="sub-header">AI-powered career fit assessment and interview preparation</div>', unsafe_allow_html=True)
    
# #     # Display uploaded files
# #     display_uploaded_files()
    
# #     # Welcome message or chat interface
# #     if not st.session_state.resume_text:
# #         st.info("👈 Get started by uploading your resume in the sidebar!")
        
# #         # Show features
# #         st.markdown("### ✨ Features")
# #         col1, col2, col3 = st.columns(3)
        
# #         with col1:
# #             st.markdown("""
# #             **📊 Career Fit Assessment**
# #             - Analyze how well you match job requirements
# #             - Get percentage fit scores
# #             - Identify your strongest matches
# #             """)
        
# #         with col2:
# #             st.markdown("""
# #             **🎓 Skills Gap Analysis**
# #             - Discover missing skills
# #             - Understand technical and soft skill gaps
# #             - Get learning recommendations
# #             """)
        
# #         with col3:
# #             st.markdown("""
# #             **💼 Interview Preparation**
# #             - Get targeted interview questions
# #             - Learn what to emphasize
# #             - Prepare for specific roles
# #             """)
        
# #         st.markdown("---")
        
# #         # Instructions
# #         st.markdown("### 📖 How to Use")
# #         st.markdown("""
# #         1. **Configure API Key**: Enter your OpenAI API key in the sidebar
# #         2. **Upload Resume**: Upload your resume (PDF, DOCX, or TXT format)
# #         3. **Upload Job Postings**: Upload one or more job postings you're interested in
# #         4. **Ask Questions**: Use the chat interface to ask about your career fit, skills gaps, or interview preparation
# #         5. **Get Insights**: Receive personalized, actionable advice based on your documents
# #         """)
# #     else:
# #         # Display chat interface
# #         display_chat_interface()
        
# #         # Quick analysis buttons
# #         if st.session_state.job_postings and st.session_state.assistant:
# #             st.markdown("---")
# #             st.markdown("### 🚀 Quick Actions")
            
# #             cols = st.columns(min(len(st.session_state.job_postings), 3))
            
# #             for idx, (job_num, job_data) in enumerate(st.session_state.job_postings.items()):
# #                 with cols[idx % 3]:
# #                     if st.button(f"Analyze Job #{job_num}", key=f"analyze_{job_num}"):
# #                         question = f"Please provide a detailed analysis of my fit for Job #{job_num}. Include: 1) Overall fit assessment, 2) My key strengths for this role, 3) Skills gaps I need to address, and 4) Specific recommendations for my application and interview preparation."
# #                         handle_user_message(question)


# # def main():
# #     """Main application function."""
# #     initialize_session_state()
# #     sidebar_config()
# #     main_content()


# # if __name__ == "__main__":
# #     main()


# """
# Career Intelligence Assistant - Streamlit Application
# RAG-powered (ChromaDB) career fit assessment and interview preparation.
# """

# import streamlit as st
# import os
# from typing import Dict, List
# from dotenv import load_dotenv

# # Load .env from project root
# load_dotenv()

# from utils.document_parser import DocumentParser
# from utils.llm_helper import CareerIntelligenceAssistant


# # ── Page config ────────────────────────────────────────────────────────────────
# st.set_page_config(
#     page_title="Career Intelligence Assistant",
#     page_icon="🎯",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# st.markdown("""
#     <style>
#     .main-header { font-size:2.5rem; font-weight:bold; color:#1E88E5; text-align:center; padding:1rem 0; }
#     .sub-header  { font-size:1.2rem; color:#666; text-align:center; margin-bottom:2rem; }
#     .chat-message { padding:1rem; border-radius:0.5rem; margin:0.5rem 0; }
#     .user-message      { background-color:#e3f2fd; }
#     .assistant-message { background-color:#f5f5f5; }
#     .stButton>button { width:100%; }
#     .rag-badge { background:#e8f5e9; color:#2e7d32; padding:2px 8px;
#                  border-radius:12px; font-size:0.75rem; font-weight:600; }
#     </style>
# """, unsafe_allow_html=True)


# # ── Session state ──────────────────────────────────────────────────────────────
# def initialize_session_state():
#     defaults = {
#         'resume_text': None,
#         'resume_filename': None,
#         'resume_indexed': False,
#         'job_postings': {},       # {job_num: {"name": str, "content": str, "indexed": bool}}
#         'conversation_history': [],
#         'assistant': None,
#         'job_counter': 0,
#     }
#     for key, val in defaults.items():
#         if key not in st.session_state:
#             st.session_state[key] = val

#     # Try to init assistant from .env key on first load
#     if st.session_state.assistant is None:
#         api_key = os.getenv('OPENAI_API_KEY')
#         if api_key:
#             try:
#                 st.session_state.assistant = CareerIntelligenceAssistant(api_key=api_key)
#             except Exception:
#                 st.session_state.assistant = None


# # ── Helpers ────────────────────────────────────────────────────────────────────
# def parse_and_index_resume(uploaded_file) -> bool:
#     """Parse resume, chunk it, and index into ChromaDB."""
#     try:
#         file_bytes = uploaded_file.read()
#         text = DocumentParser.parse_file(file_bytes, uploaded_file.name)
#         chunks = DocumentParser.chunk_text(text)

#         st.session_state.resume_text = text
#         st.session_state.resume_filename = uploaded_file.name
#         st.session_state.resume_indexed = False

#         if st.session_state.assistant:
#             st.session_state.assistant.index_resume(chunks)
#             st.session_state.resume_indexed = True

#         return True
#     except Exception as e:
#         st.error(f"Error parsing resume: {str(e)}")
#         return False


# def parse_and_index_job(uploaded_file) -> bool:
#     """Parse a job posting, chunk it, and index into ChromaDB."""
#     try:
#         file_bytes = uploaded_file.read()
#         text = DocumentParser.parse_file(file_bytes, uploaded_file.name)
#         chunks = DocumentParser.chunk_text(text)

#         st.session_state.job_counter += 1
#         job_num = st.session_state.job_counter
#         indexed = False

#         if st.session_state.assistant:
#             st.session_state.assistant.index_job(chunks, job_num, uploaded_file.name)
#             indexed = True

#         st.session_state.job_postings[job_num] = {
#             "name": uploaded_file.name,
#             "content": text,
#             "indexed": indexed,
#             "chunks": len(chunks),
#         }
#         return True
#     except Exception as e:
#         st.error(f"Error parsing {uploaded_file.name}: {str(e)}")
#         return False


# def reindex_all():
#     """Re-index all documents after API key is set."""
#     assistant = st.session_state.assistant
#     if not assistant:
#         return

#     # Re-index resume
#     if st.session_state.resume_text and not st.session_state.resume_indexed:
#         chunks = DocumentParser.chunk_text(st.session_state.resume_text)
#         assistant.index_resume(chunks)
#         st.session_state.resume_indexed = True

#     # Re-index jobs
#     for job_num, job_data in st.session_state.job_postings.items():
#         if not job_data.get("indexed"):
#             chunks = DocumentParser.chunk_text(job_data["content"])
#             assistant.index_job(chunks, job_num, job_data["name"])
#             st.session_state.job_postings[job_num]["indexed"] = True


# def handle_user_message(user_message: str):
#     if not st.session_state.resume_text:
#         st.error("⚠️ Please upload your resume first!")
#         return
#     if not st.session_state.assistant:
#         st.error("⚠️ Please configure your OpenAI API key!")
#         return

#     st.session_state.conversation_history.append({"role": "user", "content": user_message})

#     with st.spinner("🔍 Retrieving relevant context & generating response..."):
#         response = st.session_state.assistant.get_response(
#             resume=st.session_state.resume_text,
#             job_postings=st.session_state.job_postings,
#             conversation_history=st.session_state.conversation_history[:-1],
#             user_message=user_message
#         )

#     st.session_state.conversation_history.append({"role": "assistant", "content": response})
#     st.rerun()


# # ── Sidebar ────────────────────────────────────────────────────────────────────
# def sidebar_config():
#     st.sidebar.markdown("## 🎯 Career Intelligence Assistant")
#     st.sidebar.markdown('<span class="rag-badge">⚡ RAG · ChromaDB</span>', unsafe_allow_html=True)
#     st.sidebar.markdown("---")

#     # API Key
#     st.sidebar.markdown("### 🔑 API Configuration")
#     api_key = st.sidebar.text_input(
#         "OpenAI API Key",
#         value=os.getenv('OPENAI_API_KEY', ''),
#         type="password",
#         help="Reads from .env automatically if set"
#     )

#     if api_key:
#         os.environ['OPENAI_API_KEY'] = api_key
#         if not st.session_state.assistant:
#             try:
#                 st.session_state.assistant = CareerIntelligenceAssistant(api_key=api_key)
#                 reindex_all()   # index any docs uploaded before key was set
#                 st.sidebar.success("✅ API key configured!")
#             except Exception as e:
#                 st.sidebar.error(f"❌ {str(e)}")
#         else:
#             st.sidebar.success("✅ API key active")
#     else:
#         st.sidebar.warning("⚠️ API key required for AI features")

#     st.sidebar.markdown("---")

#     # Resume upload
#     st.sidebar.markdown("### 📄 Upload Resume")
#     resume_file = st.sidebar.file_uploader(
#         "Upload your resume", type=['pdf', 'docx', 'txt'], key="resume_uploader"
#     )
#     if resume_file:
#         if st.sidebar.button("Parse & Index Resume", key="parse_resume"):
#             with st.spinner("Parsing & indexing resume into ChromaDB..."):
#                 if parse_and_index_resume(resume_file):
#                     status = "✅ Indexed into ChromaDB" if st.session_state.resume_indexed else "✅ Parsed (will index after API key set)"
#                     st.sidebar.success(status)
#                     st.rerun()

#     st.sidebar.markdown("---")

#     # Job postings upload
#     st.sidebar.markdown("### 📋 Upload Job Postings")
#     job_files = st.sidebar.file_uploader(
#         "Upload job postings (multiple)", type=['pdf', 'docx', 'txt'],
#         accept_multiple_files=True, key="job_uploader"
#     )
#     if job_files:
#         if st.sidebar.button("Parse & Index Jobs", key="parse_jobs"):
#             with st.spinner("Parsing & indexing job postings..."):
#                 for jf in job_files:
#                     if parse_and_index_job(jf):
#                         st.sidebar.success(f"✅ Indexed: {jf.name}")
#             st.rerun()

#     st.sidebar.markdown("---")

#     # Clear controls
#     st.sidebar.markdown("### 🗑️ Clear Data")
#     c1, c2 = st.sidebar.columns(2)
#     with c1:
#         if st.button("Clear Chat", key="clear_chat"):
#             st.session_state.conversation_history = []
#             st.rerun()
#     with c2:
#         if st.button("Clear All", key="clear_all"):
#             if st.session_state.assistant:
#                 st.session_state.assistant.reset_store()
#             st.session_state.resume_text = None
#             st.session_state.resume_filename = None
#             st.session_state.resume_indexed = False
#             st.session_state.job_postings = {}
#             st.session_state.conversation_history = []
#             st.session_state.job_counter = 0
#             st.rerun()

#     st.sidebar.markdown("---")
#     st.sidebar.markdown("### 💡 Example Questions")
#     st.sidebar.markdown("""
# - What skills am I missing for Job #1?
# - How does my experience align with Job #2?
# - Which job is the best fit for me?
# - Help me prepare for an interview for Job #1
# - What should I emphasize in my cover letter?
#     """)


# # ── Main content ───────────────────────────────────────────────────────────────
# def display_uploaded_files():
#     st.markdown("### 📄 Indexed Documents")
#     c1, c2 = st.columns(2)

#     with c1:
#         st.markdown("**Resume:**")
#         if st.session_state.resume_filename:
#             badge = "🟢 Indexed" if st.session_state.resume_indexed else "🟡 Parsed (not indexed)"
#             st.markdown(f"✅ {st.session_state.resume_filename}  `{badge}`")
#         else:
#             st.markdown("❌ No resume uploaded")

#     with c2:
#         st.markdown("**Job Postings:**")
#         if st.session_state.job_postings:
#             for num, data in st.session_state.job_postings.items():
#                 badge = "🟢 Indexed" if data.get("indexed") else "🟡 Parsed"
#                 chunks = data.get("chunks", "?")
#                 st.markdown(f"✅ Job #{num}: {data['name']}  `{badge}` · {chunks} chunks")
#         else:
#             st.markdown("❌ No job postings uploaded")

#     st.markdown("---")


# def display_chat_interface():
#     st.markdown("### 💬 Ask Questions")
#     for msg in st.session_state.conversation_history:
#         css_class = "user-message" if msg["role"] == "user" else "assistant-message"
#         label = "You" if msg["role"] == "user" else "Assistant"
#         st.markdown(
#             f'<div class="chat-message {css_class}"><strong>{label}:</strong> {msg["content"]}</div>',
#             unsafe_allow_html=True
#         )

#     user_input = st.chat_input("Ask about career fit, skill gaps, interview prep…")
#     if user_input:
#         handle_user_message(user_input)


# def main_content():
#     st.markdown('<div class="main-header">🎯 Career Intelligence Assistant</div>', unsafe_allow_html=True)
#     st.markdown('<div class="sub-header">RAG-powered · ChromaDB · GPT-4o-mini</div>', unsafe_allow_html=True)

#     display_uploaded_files()

#     if not st.session_state.resume_text:
#         st.info("👈 Upload your resume in the sidebar to get started!")

#         col1, col2, col3 = st.columns(3)
#         with col1:
#             st.markdown("""
# **📊 Career Fit Assessment**
# - Semantic skill matching via RAG
# - Fit scores per job posting
# - Ranked job recommendations
# """)
#         with col2:
#             st.markdown("""
# **🎓 Skills Gap Analysis**
# - Precise gap detection from JD chunks
# - Hard & soft skill breakdown
# - Learning path suggestions
# """)
#         with col3:
#             st.markdown("""
# **💼 Interview Preparation**
# - Role-specific question generation
# - Talking points from your resume
# - Targeted preparation advice
# """)

#         st.markdown("---")
#         st.markdown("### 📖 How It Works (RAG Pipeline)")
#         st.markdown("""
# 1. **Upload & Parse** — Resume and JDs are parsed from PDF/DOCX/TXT
# 2. **Chunk** — Documents are split into overlapping 500-char chunks
# 3. **Embed & Index** — Chunks are embedded via OpenAI and stored in **ChromaDB**
# 4. **Query** — Your question is embedded and matched against relevant chunks
# 5. **Generate** — Only the most relevant chunks are sent to GPT-4o-mini → precise, cost-efficient answers
# """)
#     else:
#         display_chat_interface()

#         if st.session_state.job_postings and st.session_state.assistant:
#             st.markdown("---")
#             st.markdown("### 🚀 Quick Analysis")
#             cols = st.columns(min(len(st.session_state.job_postings), 3))
#             for idx, (job_num, job_data) in enumerate(st.session_state.job_postings.items()):
#                 with cols[idx % 3]:
#                     if st.button(f"Analyze Job #{job_num}", key=f"analyze_{job_num}"):
#                         with st.spinner(f"Running RAG analysis for Job #{job_num}..."):
#                             analysis = st.session_state.assistant.get_quick_analysis(
#                                 job_num=job_num,
#                                 job_name=job_data["name"]
#                             )
#                         st.session_state.conversation_history.append({
#                             "role": "user",
#                             "content": f"Quick analysis for Job #{job_num}: {job_data['name']}"
#                         })
#                         st.session_state.conversation_history.append({
#                             "role": "assistant",
#                             "content": analysis
#                         })
#                         st.rerun()


# # ── Entry point ────────────────────────────────────────────────────────────────
# def main():
#     initialize_session_state()
#     sidebar_config()
#     main_content()


# if __name__ == "__main__":
#     main()


"""
Career Intelligence Assistant - Streamlit Application
RAG-powered (ChromaDB) career fit assessment and interview preparation.
"""

import streamlit as st
import os
import logging
import time
from typing import Dict, List, Optional
from datetime import datetime
import json
from dotenv import load_dotenv

load_dotenv()

from utils.document_parser import DocumentParser
from utils.llm_helper import CareerIntelligenceAssistant


# ── Logging ────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('career_assistant.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# ── Page config ────
st.set_page_config(
    page_title="Career Intelligence Assistant",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-header { font-size:2.5rem; font-weight:bold; color:#1E88E5; text-align:center; padding:1rem 0; }
    .sub-header  { font-size:1.2rem; color:#666; text-align:center; margin-bottom:2rem; }
    .chat-message { padding:1rem; border-radius:0.5rem; margin:0.5rem 0; }
    .user-message      { background-color:#e3f2fd; }
    .assistant-message { background-color:#f5f5f5; }
    .stButton>button { width:100%; }
    .rag-badge { background:#e8f5e9; color:#2e7d32; padding:2px 8px;
                 border-radius:12px; font-size:0.75rem; font-weight:600; }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)


# ── Guardrails ────
class Guardrails:
    """Input/output validation and safety checks."""

    BLOCKED_PATTERNS = [
        r'(?i)how to (hack|cheat|scam|bypass|exploit)',
        r'(?i)illegal (ways|methods|activities)',
        r'(?i)fake (resume|experience|credentials)',
        r'(?i)lie about',
        r'(?i)fraud|scam|dishonest',
    ]

    SENSITIVE_PATTERNS = [
        (r'\b\d{3}-\d{2}-\d{4}\b', '[REDACTED SSN]'),
        (r'\b\d{9}\b', '[REDACTED SSN]'),
        (r'\b[\w\.-]+@[\w\.-]+\.\w+\b', '[REDACTED EMAIL]'),
        (r'\b\d{10}\b', '[REDACTED PHONE]'),
        (r'\b\d{3}-\d{3}-\d{4}\b', '[REDACTED PHONE]'),
    ]

    @classmethod
    def validate_input(cls, user_message: str) -> tuple[bool, str]:
        import re
        for pattern in cls.BLOCKED_PATTERNS:
            if re.search(pattern, user_message):
                logger.warning(f"Blocked inappropriate query: {user_message[:50]}...")
                return False, "I can only help with legitimate career advice and interview preparation."
        return True, ""

    @classmethod
    def sanitize_output(cls, response: str) -> str:
        import re
        for pattern, replacement in cls.SENSITIVE_PATTERNS:
            response = re.sub(pattern, replacement, response)
        return response


# ── Session state ────
def initialize_session_state():
    defaults = {
        'resume_text': None,
        'resume_filename': None,
        'resume_indexed': False,
        'resume_chunks': 0,
        'job_postings': {},
        'indexed_job_files': set(),   # deduplication tracker
        'conversation_history': [],
        'assistant': None,
        'job_counter': 0,
        'query_count': 0,
        'total_latency': 0,
        'last_resume_file': None,
        'pending_analysis': None,     # (job_num, job_name) set on button click
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

    if st.session_state.assistant is None:
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            try:
                st.session_state.assistant = CareerIntelligenceAssistant(api_key=api_key)
                logger.info("Assistant initialized from .env")
            except Exception as e:
                logger.error(f"Failed to initialize assistant: {str(e)}")


# ── Document helpers ────
def parse_and_index_resume(uploaded_file) -> bool:
    try:
        start = time.time()
        text = DocumentParser.parse_file(uploaded_file.read(), uploaded_file.name)
        chunks = DocumentParser.chunk_text(text, chunk_size=500, chunk_overlap=50)

        st.session_state.resume_text = text
        st.session_state.resume_filename = uploaded_file.name
        st.session_state.resume_chunks = len(chunks)
        st.session_state.resume_indexed = False

        if st.session_state.assistant:
            success = st.session_state.assistant.index_resume(chunks)
            if success:
                st.session_state.resume_indexed = True
                logger.info(f"Resume indexed: {uploaded_file.name}, {len(chunks)} chunks, {time.time()-start:.2f}s")
            else:
                st.error("Failed to index resume. Check logs.")
                return False
        return True
    except Exception as e:
        logger.error(f"Error parsing resume: {str(e)}")
        st.error(f"Error parsing resume: {str(e)}")
        return False


def parse_and_index_job(uploaded_file) -> bool:
    try:
        # Skip if already indexed this session
        if uploaded_file.name in st.session_state.indexed_job_files:
            logger.info(f"Skipping already-indexed job: {uploaded_file.name}")
            return True

        start = time.time()
        text = DocumentParser.parse_file(uploaded_file.read(), uploaded_file.name)
        chunks = DocumentParser.chunk_text(text, chunk_size=500, chunk_overlap=50)

        st.session_state.job_counter += 1
        job_num = st.session_state.job_counter
        indexed = False

        if st.session_state.assistant:
            st.session_state.assistant.index_job(chunks, job_num, uploaded_file.name)
            indexed = True
            logger.info(f"Job indexed: #{job_num} - {uploaded_file.name}, {len(chunks)} chunks, {time.time()-start:.2f}s")

        st.session_state.job_postings[job_num] = {
            "name": uploaded_file.name,
            "content": text,
            "indexed": indexed,
            "chunks": len(chunks),
        }
        st.session_state.indexed_job_files.add(uploaded_file.name)
        return True
    except Exception as e:
        logger.error(f"Error parsing {uploaded_file.name}: {str(e)}")
        st.error(f"Error parsing {uploaded_file.name}: {str(e)}")
        return False


def reindex_all():
    assistant = st.session_state.assistant
    if not assistant:
        return
    if st.session_state.resume_text and not st.session_state.resume_indexed:
        chunks = DocumentParser.chunk_text(st.session_state.resume_text)
        assistant.index_resume(chunks)
        st.session_state.resume_indexed = True

    for job_num, job_data in st.session_state.job_postings.items():
        if not job_data.get("indexed"):
            chunks = DocumentParser.chunk_text(job_data["content"])
            assistant.index_job(chunks, job_num, job_data["name"])
            st.session_state.job_postings[job_num]["indexed"] = True


def handle_user_message(user_message: str):
    is_valid, error_message = Guardrails.validate_input(user_message)
    if not is_valid:
        st.session_state.conversation_history.append({"role": "user", "content": user_message})
        st.session_state.conversation_history.append({"role": "assistant", "content": error_message})
        st.rerun()
        return

    if not st.session_state.resume_text:
        st.error("⚠️ Please upload your resume first!")
        return
    if not st.session_state.assistant:
        st.error("⚠️ Please configure your OpenAI API key!")
        return

    st.session_state.conversation_history.append({"role": "user", "content": user_message})
    st.session_state.query_count += 1

    start = time.time()
    with st.spinner("🔍 Retrieving relevant context & generating response..."):
        response = st.session_state.assistant.get_response(
            resume=st.session_state.resume_text,
            job_postings=st.session_state.job_postings,
            conversation_history=st.session_state.conversation_history[:-1],
            user_message=user_message
        )

    response = Guardrails.sanitize_output(response)
    latency = time.time() - start
    st.session_state.total_latency += latency
    logger.info(f"Query #{st.session_state.query_count}: {user_message[:50]}... | Latency: {latency:.2f}s")

    st.session_state.conversation_history.append({"role": "assistant", "content": response})
    st.rerun()


# ── Sidebar ────
def sidebar_config():
    st.sidebar.markdown("## 🎯 Career Intelligence Assistant")
    st.sidebar.markdown('<span class="rag-badge">⚡ RAG · ChromaDB · GPT-4o-mini</span>', unsafe_allow_html=True)
    st.sidebar.markdown("---")

    st.sidebar.markdown("### 🔑 API Configuration")
    api_key = st.sidebar.text_input(
        "OpenAI API Key",
        value=os.getenv('OPENAI_API_KEY', ''),
        type="password",
        help="Reads from .env automatically if set"
    )

    if api_key:
        os.environ['OPENAI_API_KEY'] = api_key
        if not st.session_state.assistant:
            try:
                with st.spinner("Initializing assistant..."):
                    st.session_state.assistant = CareerIntelligenceAssistant(api_key=api_key)
                    reindex_all()
                st.sidebar.success("✅ API key configured!")
            except Exception as e:
                st.sidebar.error(f"❌ {str(e)}")
        else:
            st.sidebar.success("✅ API key active")
    else:
        st.sidebar.warning("⚠️ API key required for AI features")

    st.sidebar.markdown("---")

    # Resume upload
    st.sidebar.markdown("### 📄 Upload Resume")
    resume_file = st.sidebar.file_uploader(
        "Upload your resume", type=['pdf', 'docx', 'txt'], key="resume_uploader"
    )
    if resume_file and resume_file.name != st.session_state.get('last_resume_file'):
        if st.sidebar.button("Parse & Index Resume", key="parse_resume"):
            with st.spinner("Parsing & indexing resume into ChromaDB..."):
                if parse_and_index_resume(resume_file):
                    st.session_state.last_resume_file = resume_file.name
                    status = "✅ Indexed into ChromaDB" if st.session_state.resume_indexed else "✅ Parsed (will index after API key set)"
                    st.sidebar.success(status)
                    st.rerun()

    st.sidebar.markdown("---")

    # Job postings upload
    st.sidebar.markdown("### 📋 Upload Job Postings")
    job_files = st.sidebar.file_uploader(
        "Upload job postings (multiple)", type=['pdf', 'docx', 'txt'],
        accept_multiple_files=True, key="job_uploader"
    )
    if job_files:
        new_files = [jf for jf in job_files if jf.name not in st.session_state.indexed_job_files]
        if new_files:
            if st.sidebar.button("Parse & Index Jobs", key="parse_jobs"):
                with st.spinner("Parsing & indexing job postings..."):
                    for jf in new_files:
                        if parse_and_index_job(jf):
                            st.sidebar.success(f"✅ Indexed: {jf.name}")
                st.rerun()
        else:
            st.sidebar.success("✅ All uploaded jobs already indexed")

    st.sidebar.markdown("---")

    if st.session_state.query_count > 0:
        st.sidebar.markdown("### 📊 Performance")
        avg_latency = st.session_state.total_latency / st.session_state.query_count
        st.sidebar.metric("Total Queries", st.session_state.query_count)
        st.sidebar.metric("Avg Response Time", f"{avg_latency:.2f}s")

    st.sidebar.markdown("---")

    st.sidebar.markdown("### 🗑️ Clear Data")
    c1, c2 = st.sidebar.columns(2)
    with c1:
        if st.button("Clear Chat", key="clear_chat"):
            st.session_state.conversation_history = []
            st.rerun()
    with c2:
        if st.button("Clear All", key="clear_all"):
            if st.session_state.assistant:
                st.session_state.assistant.reset_store()
            for key in ['resume_text', 'resume_filename', 'resume_indexed', 'resume_chunks',
                        'conversation_history', 'job_counter', 'query_count', 'total_latency',
                        'last_resume_file', 'pending_analysis']:
                st.session_state[key] = None if 'text' in key or 'filename' in key or 'file' in key else \
                                        False if 'indexed' in key else \
                                        0 if any(x in key for x in ['chunks', 'counter', 'count', 'latency']) else \
                                        [] if 'history' in key else None
            st.session_state.job_postings = {}
            st.session_state.indexed_job_files = set()
            st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💡 Example Questions")
    st.sidebar.markdown("""
- What skills am I missing for Job #1?
- How does my experience align with Job #2?
- Which job is the best fit for me?
- Help me prepare for an interview for Job #1
- What should I emphasize in my cover letter?
    """)


# ── Main content ────
def display_uploaded_files():
    st.markdown("### 📄 Indexed Documents")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Resume:**")
        if st.session_state.resume_filename:
            badge = "🟢 Indexed" if st.session_state.resume_indexed else "🟡 Parsed (not indexed)"
            chunks_info = f" · {st.session_state.resume_chunks} chunks" if st.session_state.resume_indexed else ""
            st.markdown(f"✅ {st.session_state.resume_filename}  `{badge}`{chunks_info}")
        else:
            st.markdown("❌ No resume uploaded")

    with col2:
        st.markdown("**Job Postings:**")
        if st.session_state.job_postings:
            for num, data in st.session_state.job_postings.items():
                badge = "🟢 Indexed" if data.get("indexed") else "🟡 Parsed"
                st.markdown(f"✅ Job #{num}: {data['name']}  `{badge}` · {data.get('chunks','?')} chunks")
        else:
            st.markdown("❌ No job postings uploaded")

    st.markdown("---")


def display_chat_interface():
    st.markdown("### 💬 Ask Questions")
    for msg in st.session_state.conversation_history:
        css_class = "user-message" if msg["role"] == "user" else "assistant-message"
        label = "You" if msg["role"] == "user" else "Assistant"
        st.markdown(
            f'<div class="chat-message {css_class}"><strong>{label}:</strong> {msg["content"]}</div>',
            unsafe_allow_html=True
        )
    user_input = st.chat_input("Ask about career fit, skill gaps, interview prep…")
    if user_input:
        handle_user_message(user_input)


def run_quick_analysis(job_num: int, job_name: str):
    """Execute quick analysis exactly once and append to conversation history."""
    with st.spinner(f"Running RAG analysis for Job #{job_num}..."):
        analysis = st.session_state.assistant.get_quick_analysis(
            job_num=job_num,
            job_name=job_name
        )
    st.session_state.conversation_history.append({
        "role": "user",
        "content": f"Quick analysis for Job #{job_num}: {job_name}"
    })
    st.session_state.conversation_history.append({
        "role": "assistant",
        "content": analysis
    })
    st.session_state.pending_analysis = None  # clear flag after execution


def main_content():
    st.markdown('<div class="main-header">🎯 Career Intelligence Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">RAG-powered · ChromaDB · GPT-4o-mini</div>', unsafe_allow_html=True)

    display_uploaded_files()

    if not st.session_state.resume_text:
        st.info("👈 Upload your resume in the sidebar to get started!")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="metric-card">
            <b>📊 Career Fit Assessment</b><br>
            Semantic skill matching via RAG · Fit scores · Ranked recommendations
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="metric-card">
            <b>🎓 Skills Gap Analysis</b><br>
            Precise gap detection · Hard & soft skills · Learning paths
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class="metric-card">
            <b>💼 Interview Preparation</b><br>
            Role-specific questions · Talking points · Targeted advice
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        with st.expander("🔍 How It Works (RAG Pipeline)", expanded=False):
            st.markdown("""
            1. **📄 Document Processing** — Resume and JDs parsed from PDF/DOCX/TXT
            2. **✂️ Intelligent Chunking** — Sentence-aware overlapping chunks (500 chars, 50 overlap)
            3. **🔢 Embedding & Indexing** — `text-embedding-ada-002` vectors stored in ChromaDB
            4. **🎯 Retrieval** — MMR-based top-k chunk retrieval per query
            5. **🤖 Generation** — GPT-4o-mini generates grounded responses from retrieved context
            6. **🛡️ Safety** — Input validation + PII redaction on all outputs
            """)
    else:
        # ── Two-phase button pattern: execute pending analysis BEFORE rendering buttons ──
        # This ensures analysis fires exactly once per click, not on every Streamlit rerun
        if st.session_state.pending_analysis is not None:
            job_num, job_name = st.session_state.pending_analysis
            run_quick_analysis(job_num, job_name)
            st.rerun()

        display_chat_interface()

        if st.session_state.job_postings and st.session_state.assistant:
            st.markdown("---")
            st.markdown("### 🚀 Quick Analysis")

            cols = st.columns(min(len(st.session_state.job_postings), 3))
            for idx, (job_num, job_data) in enumerate(st.session_state.job_postings.items()):
                with cols[idx % 3]:
                    if st.button(f"Analyze Job #{job_num}", key=f"btn_analyze_{job_num}"):
                        # Phase 1: set flag and rerun — analysis executes at top of next run
                        st.session_state.pending_analysis = (job_num, job_data["name"])
                        st.rerun()


# ── Entry point ────
def main():
    try:
        initialize_session_state()
        sidebar_config()
        main_content()
    except Exception as e:
        logger.error(f"Application error: {str(e)}", exc_info=True)
        st.error("An unexpected error occurred. Please check the logs.")


if __name__ == "__main__":
    main()