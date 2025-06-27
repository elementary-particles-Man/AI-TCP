# watch_and_execute.sh（擬似）
while true; do
  if [ -f new_task.json ]; then
    curl http://localhost:1234/v1/chat/completions -d @new_task.json > output.json
    mv new_task.json archive/
    notify-send "Task completed"
  fi
  sleep 2
done
