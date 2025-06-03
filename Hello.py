import streamlit as st
import openai
from datetime import datetime
import calendar
from dateutil.relativedelta import relativedelta

# Page configuration
st.set_page_config(
    page_title="Super Resume - AI Career Optimizer",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for aesthetic styling that complements the logo
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #10b981 0%, #059669 50%, #047857 100%);
        min-height: 100vh;
    }
    
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #10b981 0%, #0891b2 50%, #0e7490 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.02em;
    }
    
    .subtitle {
        text-align: center;
        color: #374151;
        font-size: 1.2rem;
        margin-bottom: 3rem;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    }
    
    .hero-section {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(8, 145, 178, 0.1) 100%);
        border-radius: 20px;
        padding: 3rem 2rem;
        margin-bottom: 2rem;
        border: 2px solid rgba(16, 185, 129, 0.3);
        backdrop-filter: blur(10px);
        text-align: center;
        box-shadow: 0 8px 32px rgba(16, 185, 129, 0.2);
    }
    
    .tab-header {
        color: #065f46;
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #10b981 0%, #0891b2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .success-box {
        padding: 1.5rem;
        border-radius: 15px;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(34, 197, 94, 0.15) 100%);
        border: 2px solid rgba(16, 185, 129, 0.4);
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(16, 185, 129, 0.2);
    }
    
    .error-box {
        padding: 1.5rem;
        border-radius: 15px;
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.1) 100%);
        border: 2px solid rgba(239, 68, 68, 0.4);
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(239, 68, 68, 0.1);
    }
    
    .info-box {
        padding: 1.5rem;
        border-radius: 15px;
        background: linear-gradient(135deg, rgba(8, 145, 178, 0.15) 0%, rgba(14, 116, 144, 0.15) 100%);
        border: 2px solid rgba(8, 145, 178, 0.4);
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(8, 145, 178, 0.2);
    }
    
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.95);
        border: 2px solid rgba(16, 185, 129, 0.3);
        border-radius: 12px;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: rgba(16, 185, 129, 0.6);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
    }
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.95);
        border: 2px solid rgba(16, 185, 129, 0.3);
        border-radius: 12px;
        backdrop-filter: blur(10px);
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: rgba(16, 185, 129, 0.8);
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
    }
    
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.95);
        border: 2px solid rgba(16, 185, 129, 0.3);
        border-radius: 12px;
        backdrop-filter: blur(10px);
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: rgba(16, 185, 129, 0.8);
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #10b981 0%, #0891b2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.6);
        background: linear-gradient(135deg, #059669 0%, #0e7490 100%);
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 0.5rem;
        margin: 1rem 0;
        border: 2px solid rgba(16, 185, 129, 0.2);
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px rgba(16, 185, 129, 0.1);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(16, 185, 129, 0.2);
        border-color: rgba(16, 185, 129, 0.4);
    }
    
    .stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(8, 145, 178, 0.1) 100%);
    border-radius: 15px;
    padding: 0.75rem;  /* Increased from 0.5rem */
    backdrop-filter: blur(10px);
    border: 2px solid rgba(16, 185, 129, 0.2);
    margin-bottom: 1rem;  /* Added space below tabs */
}

.stTabs [data-baseweb="tab"] {
    background: rgba(255, 255, 255, 0.8);
    border-radius: 10px;
    color: #065f46;
    font-weight: 500;
    font-family: 'Inter', sans-serif;
    border: 1px solid rgba(16, 185, 129, 0.2);
    transition: all 0.3s ease;
    padding: 0.75rem 1.5rem;  /* Added internal padding */
    margin: 0.25rem;  /* Added margin around each tab */
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #10b981 0%, #0891b2 100%);
    color: white;
    border-color: rgba(16, 185, 129, 0.6);
}
    
    .footer {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(8, 145, 178, 0.1) 100%);
        border-radius: 20px;
        margin-top: 3rem;
        backdrop-filter: blur(10px);
        border: 2px solid rgba(16, 185, 129, 0.3);
        box-shadow: 0 8px 32px rgba(16, 185, 129, 0.1);
    }
    
    /* Hero logo styling - centered */
    .hero-logo {
        display: block;
        margin: 0 auto 2rem auto;
        max-width: 200px;
        height: auto;
        filter: drop-shadow(0 4px 8px rgba(16, 185, 129, 0.3));
    }
    
    /* Sidebar logo styling */
    button[title^=Exit]+div [data-testid=stImage]{
        text-align: center;
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 100%;
        max-height: 60px;
        object-fit: contain;
    }
    button[title^=Exit]+div [data-testid=stImage] img{
        max-height: 60px;
        width: auto;
        object-fit: contain;
        filter: drop-shadow(0 2px 4px rgba(16, 185, 129, 0.3));
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.98) 0%, rgba(240, 253, 244, 0.98) 100%);
        backdrop-filter: blur(20px);
    }
    
    /* Radio button styling */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        padding: 1rem;
        border: 2px solid rgba(16, 185, 129, 0.2);
    }
    
    /* Multiselect styling */
    .stMultiSelect > div > div {
        background: rgba(255, 255, 255, 0.95);
        border: 2px solid rgba(16, 185, 129, 0.3);
        border-radius: 12px;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'api_keys_configured' not in st.session_state:
    st.session_state.api_keys_configured = False

# Logo configuration
LOGO_PNG = "logo1.png"
sidebar_logo = LOGO_PNG
st.logo(sidebar_logo, icon_image=LOGO_PNG)

# Sidebar section
with st.sidebar:
    # Title section with logo-matching colors
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem; padding: 1.5rem; 
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(8, 145, 178, 0.1) 100%); 
    border-radius: 15px; border: 2px solid rgba(16, 185, 129, 0.3); 
    box-shadow: 0 4px 16px rgba(16, 185, 129, 0.1);">
        <h1 style="font-family: 'Inter', sans-serif; font-weight: 700; font-size: 1.6rem; 
        background: linear-gradient(135deg, #10b981 0%, #0891b2 100%); -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; background-clip: text; margin: 0;">
        Super Resume
        </h1>
        <p style="color: #059669; font-size: 0.9rem; margin: 0.5rem 0 0 0; font-weight: 500;">
        AI-Powered Optimization
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("🔑 API Configuration")
    
    # OpenAI API Key
    openai_key = st.text_input(
        "OpenAI API Key", 
        type="password", 
        help="Enter your OpenAI API key to access GPT models"
    )
    
    # Test API connection
    if st.button("🧪 Test API Connection", key="test_api"):
        if openai_key:
            try:
                openai.api_key = openai_key
                response = openai.models.list()
                st.success("✅ OpenAI API Connected Successfully!")
            except Exception as e:
                st.error(f"❌ Connection Failed: {str(e)[:100]}...")
        else:
            st.warning("⚠️ Please enter your OpenAI API key first")
    
    # API Information
    st.markdown("---")
    st.subheader("ℹ️ API Information")
    st.markdown("""
    **OpenAI API Key Required**
    - Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
    - Usage will be charged based on OpenAI's pricing
    - GPT-4 models provide the highest quality results
    """)
    
    if st.expander("📊 Pricing Information"):
        st.markdown("""
        **OpenAI GPT-4 Pricing:**
        - Input: $0.03 per 1K tokens
        - Output: $0.06 per 1K tokens
        
        **Estimated costs per operation:**
        - Job Experience Tailoring: ~$0.10-0.30
        - Resume Optimization: ~$0.20-0.50
        
        *Actual costs may vary based on content length*
        """)
    
    if st.expander("🔒 Privacy & Security"):
        st.markdown("""
        - Your API key is not stored on our servers
        - Data is sent directly to OpenAI's API
        - No conversation history is retained
        - Review OpenAI's [Privacy Policy](https://openai.com/privacy)
        """)

# Hero Section with Centered Logo
# Use container div with custom class for styling
# Hero Section with Ghost GIF
st.markdown(
    """
    <style>
        button[title^=Exit]+div [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True
)

try:
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image("logo1.png")
except:
    st.markdown("👻", unsafe_allow_html=True)


# Helper Functions
def calculate_months_between_dates(start_month, start_year, end_month, end_year):
    """Calculate the number of months between two dates"""
    start_date = datetime(start_year, start_month, 1)
    end_date = datetime(end_year, end_month, 1)
    
    # Calculate the difference
    diff = relativedelta(end_date, start_date)
    total_months = diff.years * 12 + diff.months
    
    return total_months

def get_ai_response(prompt, api_key):
    """Get response from OpenAI GPT-4"""
    try:
        if not api_key:
            return "Error: OpenAI API key not provided"
        
        openai.api_key = api_key
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            temperature=0.7
        )
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error: {str(e)}"

# Main Tabs
st.write("Select Tabs of your choice")
tab1, tab2 = st.tabs([
    "💼 Tailor your Job Experience ", 
    "📝 Optimize your Resume based on Job Description  "
])

# Tab 1: Job Experience Tailor
with tab1:
    st.markdown('<h2 class="tab-header">💼 Tailor your Job Experience</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <p style="font-family: 'Inter', sans-serif; color: #374151; font-size: 1.1rem; margin: 0; line-height: 1.6;">
            Transform your job experiences to perfectly match specific job descriptions or industry domains. 
            Create compelling, professional narratives that highlight your relevant skills and achievements.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #065f46; font-family: 'Inter', sans-serif; margin-bottom: 1rem; font-weight: 600;">📋 Job Details</h3>
        """, unsafe_allow_html=True)
        
        # Required fields
        job_title = st.text_input("Job Title *", placeholder="e.g., Software Engineer")
        
        # Optional job description
        job_description = st.text_area(
            "Job Description (Optional)", 
            placeholder="Paste the job description here or leave empty to use domain-based tailoring...",
            height=150
        )
        
        # Domain selection
        target_domain = st.selectbox(
            "Target Domain (Optional)",
            [
                "None - General Tailoring",
                "Healthcare",
                "Supply Chain & Logistics",
                "Retail & E-commerce",
                "Financial Services & Banking",
                "Web3 & Blockchain",
                "Cryptocurrency & DeFi",
                "Software & Technology",
                "Manufacturing",
                "Real Estate",
                "Energy & Utilities",
                "Education & EdTech",
                "Media & Entertainment",
                "Telecommunications",
                "Automotive",
                "Aerospace & Defense",
                "Agriculture & Food",
                "Insurance",
                "Consulting",
                "Non-Profit",
                "Government & Public Sector",
                "Other"
            ]
        )
        
        if target_domain == "Other":
            custom_domain = st.text_input("Specify Domain")
            target_domain = custom_domain if custom_domain else "General"
        elif target_domain == "None - General Tailoring":
            target_domain = "General"
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #065f46; font-family: 'Inter', sans-serif; margin-bottom: 1rem; font-weight: 600;">📅 Experience Duration</h3>
        """, unsafe_allow_html=True)
        
        # Start date
        start_col1, start_col2 = st.columns([1, 1])
        with start_col1:
            start_month = st.selectbox(
                "Start Month *",
                list(range(1, 13)),
                format_func=lambda x: calendar.month_name[x]
            )
        with start_col2:
            start_year = st.number_input(
                "Start Year *",
                min_value=1990,
                max_value=datetime.now().year,
                value=2020
            )
        
        # End date
        end_col1, end_col2 = st.columns([1, 1])
        with end_col1:
            end_month = st.selectbox(
                "End Month *",
                list(range(1, 13)),
                format_func=lambda x: calendar.month_name[x],
                index=datetime.now().month - 1
            )
        with end_col2:
            end_year = st.number_input(
                "End Year *",
                min_value=1990,
                max_value=datetime.now().year + 1,
                value=datetime.now().year
            )
        
        # Calculate duration
        if start_year and end_year and start_month and end_month:
            total_months = calculate_months_between_dates(start_month, start_year, end_month, end_year)
            years = total_months // 12
            months = total_months % 12
            
            duration_text = []
            if years > 0:
                duration_text.append(f"{years} year{'s' if years > 1 else ''}")
            if months > 0:
                duration_text.append(f"{months} month{'s' if months > 1 else ''}")
            
            duration_display = " and ".join(duration_text) if duration_text else "0 months"
            
            st.markdown(f"""
            <div class="info-box">
                <strong style="color: #065f46;">Experience Duration:</strong> {duration_display}<br>
                <strong style="color: #065f46;">Total Months:</strong> {total_months}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Current experience input
    st.markdown("""
    <div class="feature-card">
        <h3 style="color: #065f46; font-family: 'Inter', sans-serif; margin-bottom: 1rem; font-weight: 600;">📝 Experience Information *</h3>
    """, unsafe_allow_html=True)
    
    # Option to choose between current experience or skills/prompt
    experience_option = st.radio(
        "Choose how you'd like to provide your experience information:",
        [
            "📋 Describe Current Experience", 
            "🎯 Provide Skills & Requirements"
        ],
        help="Choose whether to describe your current experience or specify skills you want to highlight"
    )
    
    if experience_option == "📋 Describe Current Experience":
        current_experience = st.text_area(
            "Describe your current experience in this role *",
            placeholder="Describe your responsibilities, achievements, technologies used, etc...",
            height=200,
            key="current_exp"
        )
        skills_prompt = ""
    else:
        skills_prompt = st.text_area(
            "Skills & Requirements to Include *",
            placeholder="List the skills, technologies, achievements, or specific requirements you want to highlight in the tailored experience. For example:\n- Programming languages: Python, JavaScript\n- Leadership experience\n- Project management\n- Specific achievements or metrics\n- Technologies or tools you want to emphasize",
            height=200,
            key="skills_prompt"
        )
        current_experience = ""
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    
    # Generate tailored experience
    if st.button("✨ Generate Tailored Experience", type="primary", key="generate_exp"):
        if not job_title or (not current_experience and not skills_prompt):
            st.error("Please fill in all required fields (Job Title and Experience Information)")
        else:
            # Check API key
            if not openai_key:
                st.error("Please enter your OpenAI API key in the sidebar first")
            else:
                # Create the prompt based on whether domain is specified or not
                if target_domain != "General":
                    if current_experience:
                        # Using current experience description
                        prompt = f"""
Please generate a tailored job experience description for the role of {job_title} in the {target_domain} industry. The tailored description should be based on the following details:

- Job Title: {job_title}
- Target Industry/Domain: {target_domain}
- Experience Duration: {duration_display}
- Job Description: {job_description if job_description else "Not provided"}
- Current Experience Description: {current_experience}

The tailored experience should:
1. Highlight relevant skills and achievements for the {target_domain} industry.
2. Incorporate {target_domain}-specific terminology and keywords.
3. Include quantifiable achievements wherever applicable.
4. Align closely with the job description requirements provided.
5. Ensure the presentation is optimized while maintaining factual accuracy.
6. Emphasize transferable skills and relevant accomplishments.

The response should be formatted as a professional experience description suitable for inclusion in a resume or LinkedIn profile.
"""
                    else:
                        # Using skills and requirements
                        prompt = f"""
Please generate a tailored job experience description for the role of {job_title} in the {target_domain} industry. The tailored description should be based on the following details:

- Job Title: {job_title}
- Target Industry/Domain: {target_domain}
- Experience Duration: {duration_display}
- Job Description: {job_description if job_description else "Not provided"}
- Skills & Requirements to Include: {skills_prompt}

Please create a professional experience description that:
1. Incorporates the specified skills and requirements naturally into a cohesive experience narrative.
2. Highlights relevant skills and achievements for the {target_domain} industry.
3. Uses {target_domain}-specific terminology and keywords.
4. Includes quantifiable achievements wherever applicable.
5. Aligns closely with the job description requirements provided.
6. Ensures the presentation is optimized while maintaining professional credibility.
7. Presents the skills and requirements as accomplished responsibilities and achievements.

The response should be formatted as a professional experience description suitable for inclusion in a resume or LinkedIn profile.
"""
                else:
                    if current_experience:
                        # Using current experience description - General
                        prompt = f"""
Please generate a tailored job experience description for the role of {job_title}. The tailored description should be based on the following details:

- Job Title: {job_title}
- Experience Duration: {duration_display}
- Job Description: {job_description if job_description else "Not provided"}
- Current Experience Description: {current_experience}

The tailored experience should:
1. Highlight relevant skills and achievements for the role.
2. Incorporate professional terminology and industry-standard keywords.
3. Include quantifiable achievements wherever applicable.
4. Align closely with the job description requirements provided.
5. Ensure the presentation is optimized while maintaining factual accuracy.
6. Emphasize transferable skills and relevant accomplishments.

The response should be formatted as a professional experience description suitable for inclusion in a resume or LinkedIn profile.
"""
                    else:
                        # Using skills and requirements - General
                        prompt = f"""
Please generate a tailored job experience description for the role of {job_title}. The tailored description should be based on the following details:

- Job Title: {job_title}
- Experience Duration: {duration_display}
- Job Description: {job_description if job_description else "Not provided"}
- Skills & Requirements to Include: {skills_prompt}

Please create a professional experience description that:
1. Incorporates the specified skills and requirements naturally into a cohesive experience narrative.
2. Highlights relevant skills and achievements for the role.
3. Uses professional terminology and industry-standard keywords.
4. Includes quantifiable achievements wherever applicable.
5. Aligns closely with the job description requirements provided.
6. Ensures the presentation is optimized while maintaining professional credibility.
7. Presents the skills and requirements as accomplished responsibilities and achievements.

The response should be formatted as a professional experience description suitable for inclusion in a resume or LinkedIn profile.
"""
                
                with st.spinner("✨ Generating your tailored experience with AI magic..."):
                    response = get_ai_response(prompt, openai_key)
                    
                    if response.startswith("Error:"):
                        st.error(response)
                    else:
                        st.success("✅ Your tailored experience is ready!")
                        
                        # Display the result
                        st.markdown('<h3 class="tab-header">🎯 Your Tailored Experience</h3>', unsafe_allow_html=True)
                        st.markdown(f"""
                        <div class="success-box">
                            <div style="font-family: 'Inter', sans-serif; line-height: 1.6; color: #065f46;">
                                {response.replace(chr(10), '<br>')}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Copy to clipboard button
                        st.text_area("📋 Copy this optimized text:", value=response, height=200, key="copy_exp")

# AI Model section
    st.markdown("""
    <div class="info-box">
        <h3 style="color: #065f46; font-family: 'Inter', sans-serif; margin-bottom: 0.5rem; font-weight: 600;">🤖 OpenAI GPT-4</h3>
        <p style="margin: 0; color: #374151; font-weight: 500;">High-quality AI responses powered by OpenAI's most advanced model</p>
    </div>
    """, unsafe_allow_html=True)


# Tab 2: Resume Optimizer
with tab2:
    st.markdown('<h2 class="tab-header">📄 Optimize your Resume based on Job Description</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <p style="font-family: 'Inter', sans-serif; color: #374151; font-size: 1.1rem; margin: 0; line-height: 1.6;">
            Optimize your entire resume based on specific job descriptions. Get intelligent keyword integration, 
            skills enhancement, and professional formatting that gets you noticed by recruiters and ATS systems.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #065f46; font-family: 'Inter', sans-serif; margin-bottom: 1rem; font-weight: 600;">📋 Job Information</h3>
        """, unsafe_allow_html=True)
        
        # Job description input
        job_description_resume = st.text_area(
            "Job Description *",
            placeholder="Paste the complete job description here...",
            height=250,
            help="Provide the full job description for the position you're applying to"
        )
        
        # Domain selection for resume
        resume_domain = st.selectbox(
            "Target Domain (Optional)",
            [
                "None - General Optimization",
                "Healthcare",
                "Supply Chain & Logistics",
                "Retail & E-commerce",
                "Financial Services & Banking",
                "Web3 & Blockchain",
                "Cryptocurrency & DeFi",
                "Software & Technology",
                "Manufacturing",
                "Real Estate",
                "Energy & Utilities",
                "Education & EdTech",
                "Media & Entertainment",
                "Telecommunications",
                "Automotive",
                "Aerospace & Defense",
                "Agriculture & Food",
                "Insurance",
                "Consulting",
                "Non-Profit",
                "Government & Public Sector",
                "Other"
            ],
            key="resume_domain"
        )
        
        if resume_domain == "Other":
            custom_resume_domain = st.text_input("Specify Domain", key="custom_resume_domain")
            resume_domain = custom_resume_domain if custom_resume_domain else "General"
        elif resume_domain == "None - General Optimization":
            resume_domain = "General"
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #065f46; font-family: 'Inter', sans-serif; margin-bottom: 1rem; font-weight: 600;">📄 Current Resume</h3>
        """, unsafe_allow_html=True)
        
        # Resume input
        current_resume = st.text_area(
            "Your Current Resume *",
            placeholder="Paste your current resume content here...",
            height=250,
            help="Provide your complete current resume text"
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Additional preferences
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #065f46; font-family: 'Inter', sans-serif; margin-bottom: 1rem; font-weight: 600;">⚙️ Optimization Preferences</h3>
        """, unsafe_allow_html=True)
        
        optimization_focus = st.multiselect(
            "Focus Areas (Optional)",
            [
                "Keywords Optimization",
                "Skills Enhancement",
                "Experience Alignment",
                "Job Title Adjustment",
                "Achievement Quantification",
                "Technical Skills",
                "Soft Skills",
                "Industry Terminology"
            ],
            default=["Keywords Optimization", "Experience Alignment"],
            help="Select areas you want to prioritize in the optimization"
        )
        
        maintain_format = st.checkbox(
            "Maintain Original Format",
            value=True,
            help="Keep the general structure and format of your original resume"
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    
    
    # Generate optimized resume
    if st.button("🚀 Optimize Resume", type="primary", key="optimize_resume"):
        if not job_description_resume or not current_resume:
            st.error("Please provide both the job description and your current resume")
        else:
            # Check API key
            if not openai_key:
                st.error("Please enter your OpenAI API key in the sidebar first")
            else:
                # Create the optimization prompt
                domain_context = f" in the {resume_domain} industry" if resume_domain != "General" else ""
                focus_areas = ", ".join(optimization_focus) if optimization_focus else "general optimization"
                format_instruction = "Maintain the original format and structure of the resume." if maintain_format else "You may restructure the resume for better presentation."
                
                prompt = f"""
You are a resume optimization AI tasked with tailoring a user's resume based on a provided job description{domain_context}. Follow these guidelines:

**Input Requirements:**
- Current Resume: {current_resume}
- Job Description: {job_description_resume}
- Target Domain: {resume_domain}
- Focus Areas: {focus_areas}

**Optimization Guidelines:**

1. **Job Title and Experience:**
   - Change the job title on the resume to align with the title in the job description if necessary
   - Adjust the experience section to reflect relevant duties and responsibilities based on the job description, while ensuring the user's original experience is recognizable

2. **Keyword Integration:**
   - Identify keywords and phrases from the job description
   - Integrate these keywords naturally into the resume, particularly in the experience, skills, and summary sections
   - Focus on {resume_domain}-specific terminology if applicable

3. **Skills Section:**
   - Analyze the skills mentioned in the job description
   - Suggest additional skills to be added to the resume, ensuring they align with the user's background and the job requirements
   - Clearly outline which skills have been added or modified

4. **Format and Structure:**
   - {format_instruction}
   - Ensure professional presentation and readability

5. **Summarization of Changes:**
   - Provide a summary of all changes made to the resume, including:
     * Modifications to the job title
     * Adjustments in the experience section
     * New keywords incorporated
     * Skills added or suggested
     * Any other significant changes

**Output Requirements:**
- Return the complete tailored resume
- Include a detailed summary of changes in a clear and concise format
- Ensure the final output maintains the integrity of the user's original experience while enhancing alignment with the target job description

Focus particularly on: {focus_areas}
"""
                
                with st.spinner("🚀 Optimizing your resume with AI intelligence..."):
                    response = get_ai_response(prompt, openai_key)
                    
                    if response.startswith("Error:"):
                        st.error(response)
                    else:
                        st.success("✅ Your resume optimization is complete!")
                        
                        # Try to split the response into optimized resume and summary
                        if "summary of changes" in response.lower() or "changes made" in response.lower():
                            # Attempt to separate the resume from the summary
                            parts = response.split("**Summary of Changes**") if "**Summary of Changes**" in response else response.split("**Changes Made**") if "**Changes Made**" in response else [response, ""]
                            
                            if len(parts) > 1:
                                optimized_resume = parts[0].strip()
                                changes_summary = parts[1].strip()
                            else:
                                optimized_resume = response
                                changes_summary = "Summary not separated - included in the optimized resume above."
                        else:
                            optimized_resume = response
                            changes_summary = "Summary not provided separately."
                        
                        # Display results in tabs
                        result_tab1, result_tab2 = st.tabs(["📄 Optimized Resume ", "📝 Summary of Changes "])
                        
                        with result_tab1:
                            st.markdown('<h3 class="tab-header">🎯 Your Optimized Resume</h3>', unsafe_allow_html=True)
                            st.markdown(f"""
                            <div class="success-box">
                                <div style="font-family: 'Inter', sans-serif; line-height: 1.6; white-space: pre-wrap; color: #065f46;">
                                    {optimized_resume}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Copy to clipboard
                            st.text_area("📋 Copy your optimized resume:", value=optimized_resume, height=400, key="optimized_resume_copy")
                        
                        with result_tab2:
                            st.markdown('<h3 class="tab-header">📋 Summary of Changes</h3>', unsafe_allow_html=True)
                            if changes_summary and changes_summary != "Summary not provided separately.":
                                st.markdown(f"""
                                <div class="info-box">
                                    <div style="font-family: 'Inter', sans-serif; line-height: 1.6; color: #065f46;">
                                        {changes_summary}
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.info("The AI included the summary within the optimized resume above.")
                            
                            # Additional analysis
                            st.markdown("""
                            <div class="feature-card">
                                <h4 style="color: #065f46; font-family: 'Inter', sans-serif; margin-bottom: 1rem; font-weight: 600;">📊 Optimization Details</h4>
                            """, unsafe_allow_html=True)
                            
                            st.markdown("**Focus Areas Applied:**")
                            for area in optimization_focus:
                                st.write(f"✅ {area}")
                            
                            if resume_domain != "General":
                                st.write(f"🎯 **Industry Focus:** {resume_domain}")
                            
                            st.write("🤖 **AI Model Used:** OpenAI GPT-4")
                            st.markdown("</div>", unsafe_allow_html=True)
    
    # AI Model section for resume
    st.markdown("""
    <div class="info-box">
        <h3 style="color: #065f46; font-family: 'Inter', sans-serif; margin-bottom: 0.5rem; font-weight: 600;">🤖 OpenAI GPT-4</h3>
        <p style="margin: 0; color: #374151; font-weight: 500;">Professional resume optimization powered by OpenAI's most advanced model</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Additional tips
    st.markdown("""
    <div class="feature-card">
        <h3 style="color: #065f46; font-family: 'Inter', sans-serif; margin-bottom: 1rem; font-weight: 600;">💡 Resume Optimization Tips</h3>
        <div style="font-family: 'Inter', sans-serif; color: #374151; line-height: 1.6;">
            <strong style="color: #059669;">For best results:</strong>
            <ul style="margin-top: 0.5rem;">
                <li><strong>Complete Job Description:</strong> Provide the full job posting for comprehensive optimization</li>
                <li><strong>Detailed Resume:</strong> Include all relevant experience, skills, and achievements</li>
                <li><strong>Domain Selection:</strong> Choose the target industry for industry-specific terminology</li>
                <li><strong>Focus Areas:</strong> Select specific areas you want to emphasize</li>
                <li><strong>Review Output:</strong> Always review and customize the optimized resume to match your voice</li>
                <li><strong>ATS Optimization:</strong> The AI automatically includes relevant keywords for applicant tracking systems</li>
                <li><strong>Multiple Versions:</strong> Create different optimized versions for different types of roles</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)


# Footer content
st.markdown("""
<div class="footer">
    <h3 style="color: #065f46; font-family: 'Inter', sans-serif; margin-bottom: 0.5rem; 
    background: linear-gradient(135deg, #10b981 0%, #0891b2 100%); -webkit-background-clip: text; 
    -webkit-text-fill-color: transparent; background-clip: text; font-weight: 700; font-size: 1.8rem;">
    Super Resume
    </h3>
    <p style="color: #6b7280; font-family: 'Inter', sans-serif; margin: 0.5rem 0;">
        AI-Powered Career Document Optimization | Built with ❤️ and Streamlit
    </p>
    <p style="color: #9ca3af; font-family: 'Inter', sans-serif; font-size: 0.9rem; margin: 0;">
        Configure your OpenAI API key in the sidebar to unlock all features
    </p>
    <div style="margin-top: 1rem; font-size: 0.8rem; color: #d1d5db;">
        <p>🔒 Secure • 🚀 Fast • 🎯 Accurate • 💼 Professional</p>
    </div>
</div>
""", unsafe_allow_html=True)