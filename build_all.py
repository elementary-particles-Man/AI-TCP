import subprocess
import datetime

print("\n🛠 AI-TCP Build System Starting...")

# ステップ1: DMCセッションHTML生成
print("\n🔧 Generating DMC session HTMLs...")
subprocess.run(["python", "tools/gen_dmc_html.py"], check=True)

# ステップ2: YAML構造マップHTML生成
print("\n🔧 Generating Structured YAML HTML...")
subprocess.run(["python", "tools/gen_structured_yaml_html.py"], check=True)

# 完了通知
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"\n✅ Build completed at {now}")
