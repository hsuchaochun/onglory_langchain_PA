#!/bin/bash

# 檢查是否已存在 relevanceai_invoke session
tmux has-session -t relevanceai_invoke 2>/dev/null
if [ $? != 0 ]; then
    # 創建新的 tmux session 並命名為 relevanceai_invoke
    tmux new-session -d -s relevanceai_invoke
    # 在 relevanceai_invoke session 中創建一個窗口運行 daily summary
    tmux send-keys -t relevanceai_invoke 'cd ~/onglory_langchain_PA/relevanceAI/relevanceai && poetry run python daily_summary_invoke.py' C-m
    # 在 relevanceai_invoke session 中創建一個窗口運行 news categorize
    tmux split-window -h -t relevanceai_invoke
    tmux send-keys -t relevanceai_invoke 'cd ~/onglory_langchain_PA/relevanceAI/relevanceai && poetry run python news_categorize_invoke.py' C-m
    echo "daily summary 和 news categorize 服務已啟動"
else
    echo "daily summary 和 news categorize 服務已在運行中"
fi

# 檢查是否已存在 news_gathering session
tmux has-session -t news_gathering 2>/dev/null
if [ $? != 0 ]; then
    # 創建新的 tmux session 並命名為 news_gathering
    tmux new-session -d -s news_gathering
    # 在 news_gathering session 中創建一個窗口運行 blockbeats api
    tmux send-keys -t news_gathering 'cd ~/onglory_langchain_PA/langchain_ws/langchain_agent/news && poetry run python blockbeats_api.py' C-m
    # 在 news_gathering session 中創建一個窗口運行 cryptopanic api
    tmux split-window -h -t news_gathering
    tmux send-keys -t news_gathering 'cd ~/onglory_langchain_PA/langchain_ws/langchain_agent/news && poetry run python cryptopanic_api.py' C-m
    echo "blockbeats api 和 cryptopanic api 服務已啟動"
else
    echo "blockbeats api 和 cryptopanic api 服務已在運行中"
fi

echo ""
echo "所有服務已啟動完成！"
echo "tmux ls                      列出所有 sessions"
echo "tmux a -t relevanceai_invoke 連接到 daily summary 和 news categorize session"
echo "tmux a -t news_gathering     連接到 blockbeats api 和 cryptopanic api session" 