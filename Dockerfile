FROM python:3.11-buster

# 作業ディレクトリを設定
WORKDIR /src

# Poetry（管理ツール）をインストール
RUN pip install poetry

# 設定ファイルを先にコピー
COPY pyproject.toml* poetry.lock* ./

# 仮想環境をプロジェクト内に作る設定
RUN poetry config virtualenvs.in-project true

# ライブラリをインストール（ここでuvicornが入ります）
RUN poetry install --no-root

# アプリ本体をコピー
COPY . .

# 起動コマンド
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]