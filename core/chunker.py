import re

def create_fixed_chunks(paragraphs, min_sentences=5):
    """
    Chia danh sách paragraph thành các khối.
    - Nếu đoạn văn ngắn (tổng số câu < min_sentences), gộp với đoạn tiếp theo.
    - Giới hạn tối đa 5 đoạn văn mỗi khối.
    - Tiêu đề 【 】 luôn bắt đầu khối mới.
    """
    chunks = []
    current_batch = []
    current_s_count = 0
    start_idx = 0
    
    for i, p in enumerate(paragraphs):
        # 1. Đếm số câu trong đoạn văn hiện tại
        sentences = re.findall(r'[^。\.!\?]+[。\.!\?]?', p)
        s_count = len(sentences) if sentences else (1 if p.strip() else 0)
        
        # 2. Quy tắc Hard Start (Tiêu đề): 
        # Chỉ ngắt khối khi gặp tiêu đề NẾU khối hiện tại đã hòm hòm (ít nhất 3 câu).
        # Điều này giúp tránh việc tiêu đề bị tách rời khỏi đoạn văn ngắn ngay sau nó.
        if p.strip().startswith("【") and current_batch and current_s_count >= 3:
            chunks.append({
                'text': "\n\n".join(current_batch),
                'p_range': (start_idx, i - 1)
            })
            current_batch = []
            current_s_count = 0
            start_idx = i
            
        current_batch.append(p)
        current_s_count += s_count
        
        # 3. Điều kiện ngắt khối:
        # - Đã đủ số câu tối thiểu (đoạn không còn "ngắn")
        # - HOẶC đã đạt giới hạn tối đa 5 đoạn văn
        if current_s_count >= min_sentences or len(current_batch) >= 5:
            chunks.append({
                'text': "\n\n".join(current_batch),
                'p_range': (start_idx, i)
            })
            current_batch = []
            current_s_count = 0
            start_idx = i + 1
            
    # Xử lý phần dư cuối cùng
    if current_batch:
        chunks.append({
            'text': "\n\n".join(current_batch),
            'p_range': (start_idx, len(paragraphs) - 1)
        })
        
    return chunks
