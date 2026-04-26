from google import genai
from core.config_manager import load_config
from core.glossary_manager import get_domains

def _generate_content(prompt: str, provider: str, api_key: str | None, model_name: str) -> str:
    """Factory method to call the appropriate AI Provider."""
    if not api_key:
        raise ValueError(f"API Key cho {provider} bị trống. Vui lòng cài đặt trong Settings.")
        
    if provider == "Google Gemini":
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )
        text = response.text
        if text is None:
            raise ValueError("Google Gemini trả về kết quả rỗng.")
        return text.strip()
        
    elif provider == "OpenAI":
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message.content
        if content is None:
            raise ValueError("OpenAI trả về kết quả rỗng.")
        return content.strip()
        
    elif provider == "Anthropic":
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=model_name,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        # Dùng isinstance để type checker thu hẹp kiểu chính xác
        text_block = next((b for b in response.content if isinstance(b, anthropic.types.TextBlock)), None)
        if text_block is None:
            raise ValueError("Anthropic trả về kết quả rỗng.")
        return text_block.text.strip()
        
    else:
        raise ValueError(f"Provider {provider} không được hỗ trợ.")

def detect_domain(text: str) -> str:
    config = load_config()
    provider = config.get("provider_detector", "Google Gemini")
    api_key = config.get("detector_api_key")
    model_name = config.get("model_detector", "gemini-1.5-flash")
    
    existing_domains = get_domains()
    domain_list_str = ", ".join(existing_domains) if existing_domains else "Chưa có lĩnh vực nào"
    
    prompt = f"Phân loại lĩnh vực văn bản tiếng Nhật sau. Đã có: [{domain_list_str}]. Trả về 1 tên lĩnh vực cũ hoặc mới. Chỉ 1-2 từ, tuyệt đối không giải thích.\nText: {text[:150]}"
    
    return _generate_content(prompt, provider, api_key, model_name)

def extract_terms(text: str, domain: str) -> dict[str, str]:
    """Sử dụng AI để trích xuất các thuật ngữ chuyên ngành từ văn bản."""
    config = load_config()
    provider = config.get("provider_detector", "Google Gemini")
    api_key = config.get("detector_api_key")
    model_name = config.get("model_detector", "gemini-1.5-flash")
    
    prompt = f"""Bạn là một chuyên gia ngôn ngữ. Hãy trích xuất các thuật ngữ chuyên ngành tiếng Nhật (Technical Terms) 
từ văn bản sau thuộc lĩnh vực {domain}. 
YÊU CẦU:
1. Chỉ trích xuất các từ chuyên môn, tên riêng hoặc thuật ngữ quan trọng.
2. Cung cấp bản dịch tiếng Việt tương ứng cho mỗi thuật ngữ.
3. KHÔNG TRÙNG LẶP: Đảm bảo danh sách không có từ nào lặp lại.
4. LÀM SẠCH: Loại bỏ mọi khoảng trắng thừa ở hai đầu của từ.
5. Trả về kết quả dưới dạng JSON: {{"tiếng Nhật": "tiếng Việt", ...}}
6. Tuyệt đối không giải thích gì thêm.

Văn bản:
{text[:2000]}"""

    res_raw = _generate_content(prompt, provider, api_key, model_name)
    
    import json
    import re
    try:
        # Làm sạch kết quả nếu AI trả về kèm markdown ```json
        clean_json = re.search(r'\{.*\}', res_raw, re.DOTALL)
        if clean_json:
            return json.loads(clean_json.group())
        return json.loads(res_raw)
    except:
        return {}

def get_review_prompt(sentences: list[str], translations: list[str], domain: str, glossary: dict[str, str]) -> str:
    """Tạo chuỗi Prompt cho bước Review/Biên tập lại."""
    combined_text = "".join(sentences)
    active_glossary = {ja: vi for ja, vi in glossary.items() if ja.strip() in combined_text}
    
    input_text = "\n".join([f"[{i+1}] Gốc: {s}\nDịch: {translations[i]}" for i, s in enumerate(sentences)])
    glossary_str = ", ".join([f"{ja} ({vi})" for ja, vi in active_glossary.items()])
    
    prompt = f"""Bạn là một Biên dịch viên cấp cao chuyên ngành {domain}. 
Hãy rà soát và hiệu đính bản dịch sau đây để đạt chất lượng xuất bản cao nhất.

YÊU CẦU BIÊN TẬP:
1. ĐẢM BẢO THUẬT NGỮ: Kiểm tra xem các thuật ngữ sau đã được dùng đúng chưa: {glossary_str if glossary_str else "N/A"}
2. VĂN PHONG: Chỉnh sửa để câu văn mượt mà, tự nhiên, mang đậm sắc thái chuyên ngành tiếng Việt.
3. CHÍNH XÁC: So sánh câu gốc và câu dịch để đảm bảo không sót ý, không dịch sai ngữ pháp.
4. GIỮ ĐỊNH DẠNG: Giữ nguyên định dạng Markdown và đánh số [1], [2]...

Nội dung cần Review:
{input_text}"""
    return prompt

def get_translation_prompt(sentences: list[str], domain: str, glossary: dict[str, str]) -> str:
    """Tạo chuỗi Prompt hoàn chỉnh cho danh sách các đoạn văn."""
    combined_text = "".join(sentences)
    active_glossary = {ja: vi for ja, vi in glossary.items() if ja.strip() in combined_text}
    
    input_text = "\n".join([f"[{i+1}] {s}" for i, s in enumerate(sentences)])
    glossary_str = "\n".join([f"- {ja} -> {vi}" for ja, vi in active_glossary.items()])
    
    prompt = f"""Bạn là một dịch giả chuyên nghiệp. Hãy dịch danh sách các đoạn văn Markdown sau từ tiếng Nhật SANG TIẾNG VIỆT.
Văn bản thuộc lĩnh vực: {domain}.

QUY TẮC BẮT BUỘC (STRICT RULES):
1. NGÔN NGỮ ĐẦU RA: BẮT BUỘC trả về kết quả bằng TIẾNG VIỆT. Tuyệt đối không trả về tiếng Anh hay ngôn ngữ khác.
2. TUÂN THỦ THUẬT NGỮ: Bạn PHẢI sử dụng đúng các cặp thuật ngữ dưới đây:
{glossary_str if glossary_str else "(Không có thuật ngữ cụ thể, hãy dịch theo ngữ cảnh chuyên ngành)"}

3. GIỮ NGUYÊN ĐỊNH DẠNG: Tuyệt đối giữ nguyên Markdown (**, *, _, #) và các ký hiệu đặc biệt như 【 】, 「 」, 『 』. KHÔNG ĐƯỢC thay thế 【 】 bằng [ ].
4. GIỮ CẤU TRÚC DÒNG: Nếu trong một đoạn văn có xuống dòng, hãy giữ nguyên vị trí xuống dòng đó.
5. SỐ LƯỢNG: Trả về đúng {len(sentences)} đoạn văn, bắt đầu bằng [1], [2],... để phân tách.
6. KHÔNG GIẢI THÍCH: Chỉ trả về bản dịch tiếng Việt.

Văn bản gốc:
{input_text}"""
    return prompt

def translate_and_review(sentences: list[str], domain: str, glossary: dict[str, str]) -> list[str]:
    """Dịch và Review một nhóm các đoạn văn (dưới dạng Markdown)."""
    config = load_config()
    
    # --- TRANSLATE ---
    provider_trans = config.get("provider_translator", "Google Gemini")
    api_key_trans = config.get("translator_api_key")
    model_trans = config.get("model_translator", "gemini-1.5-flash")
    
    prompt_trans = get_translation_prompt(sentences, domain, glossary)
    draft_vi_raw = _generate_content(prompt_trans, provider_trans, api_key_trans, model_trans)
    
    # --- REVIEW ---
    provider_rev = config.get("provider_reviewer", "Google Gemini")
    api_key_rev = config.get("reviewer_api_key") or api_key_trans
    model_rev = config.get("model_reviewer", "gemini-1.5-pro")
    
    # Lấy lại active_glossary để review
    combined_text = "".join(sentences)
    active_glossary = {ja: vi for ja, vi in glossary.items() if ja.strip() in combined_text}
    
    prompt_rev = f"""Bạn là một Biên dịch viên cấp cao. Hãy rà soát bản dịch sau để đảm bảo:
1. Đảm bảo ngôn ngữ là TIẾNG VIỆT hoàn toàn (BẮT BUỘC).
2. Độ chính xác về thuật ngữ (BẮT BUỘC: {", ".join(active_glossary.values()) if active_glossary else "N/A"}).
3. Văn phong mượt mà, tự nhiên nhưng vẫn trang trọng.
4. Giữ nguyên các ký hiệu đặc biệt (【 】, 「 」...) và Markdown. Tuyệt đối không đổi 【 】 thành [ ].
5. Giữ nguyên cấu trúc xuống dòng bên trong mỗi đoạn.
6. Trả về đúng {len(sentences)} đoạn văn, bắt đầu bằng [1], [2]...

Bản dịch cần rà soát (phải là tiếng Việt):
{draft_vi_raw}"""

    final_vi_raw = _generate_content(prompt_rev, provider_rev, api_key_rev, model_rev)
    
    # Parse kết quả
    final_list = []
    import re
    matches = re.findall(r"\[\d+\]\s*(.*?)(?=\n\[\d+\]|$)", final_vi_raw, re.DOTALL)
    
    if len(matches) == len(sentences):
        final_list = [m.strip() for m in matches]
    else:
        # Fallback 1: Thử tìm theo dòng có chứa [1], [2]...
        final_list = []
        for i in range(1, len(sentences) + 1):
            pattern = rf"\[{i}\]\s*(.*?)(?=\n\[{i+1}\]|$)"
            match = re.search(pattern, final_vi_raw, re.DOTALL)
            if match:
                final_list.append(match.group(1).strip())
            else:
                final_list.append("(Lỗi định dạng AI)")
    
    # Đảm bảo đủ số lượng
    while len(final_list) < len(sentences):
        final_list.append("(Thiếu dữ liệu dịch)")
            
    return final_list
