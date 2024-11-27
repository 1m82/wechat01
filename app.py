import streamlit as st
import requests
import json

def send_wxpusher_message(app_token, uids, message):
    """发送微信通知"""
    url = "https://wxpusher.zjiecode.com/api/send/message"
    data = {
        "appToken": app_token,
        "content": message,
        "contentType": 1,
        "uids": uids
    }
    
    try:
        response = requests.post(url, json=data)
        result = response.json()
        if result.get("code") == 1000:
            return True, "通知发送成功！"
        else:
            return False, f"发送失败：{result.get('msg')}"
    except Exception as e:
        return False, f"发送错误：{str(e)}"

def main():
    st.set_page_config(
        page_title="挪车通知系统",
        page_icon="🚗",
        layout="centered"
    )
    
    # 配置信息（建议使用环境变量或 st.secrets 存储）
    PHONE = "1**********"  # 车主电话
    WXPUSHER_APP_TOKEN = "AT_****************"  # WxPusher APP Token
    WXPUSHER_UIDS = ["UID_****************"]  # 接收者的UID

    # 页面标题
    st.title("🚗 挪车通知系统")
    st.markdown("---")

    # 创建两列布局
    col1, col2 = st.columns(2)

    with col1:
        # 微信通知部分
        st.subheader("📱 微信通知")
        default_message = "您好，有人需要您挪车，请及时处理。"
        message = st.text_area("通知内容", value=default_message, height=100)
        
        if st.button("发送微信通知", type="primary", use_container_width=True):
            if message.strip():
                success, msg = send_wxpusher_message(
                    WXPUSHER_APP_TOKEN,
                    WXPUSHER_UIDS,
                    message
                )
                if success:
                    st.success(msg)
                else:
                    st.error(msg)
            else:
                st.warning("请输入通知内容")

    with col2:
        # 电话通知部分
        st.subheader("☎️ 电话通知")
        st.markdown(f"""
        <div style='text-align: center; padding: 20px;'>
            <a href='tel:{PHONE}' target='_blank' 
               style='text-decoration: none;'>
                <button style='
                    padding: 10px 20px;
                    background-color: #17a2b8;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                '>
                拨打电话
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        st.info(f"点击按钮将拨打电话：{PHONE}")

    # 添加页面底部信息
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <small>请合理使用通知功能，避免打扰车主</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
