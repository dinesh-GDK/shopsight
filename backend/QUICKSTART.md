# ShopSight Backend - Quick Start

## 🚀 One-Command Setup

```bash
./start.sh
```

That's it! The script will:
1. Check for conda installation
2. Create/activate the `shopsight` environment
3. Install all dependencies
4. Check Ollama connection
5. Start the FastAPI server

## 📋 Prerequisites

Make sure you have:
- ✅ Conda installed (Miniconda or Anaconda)
- ✅ Ollama running (`ollama serve` in another terminal)
- ✅ Llama 3.2 model downloaded (`ollama pull llama3.2`)

## 🔧 Manual Commands

If you prefer manual control:

```bash
# 1. Create conda environment
conda env create -f environment.yml

# 2. Activate environment
conda activate shopsight

# 3. Create .env file
cp .env.example .env

# 4. Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🌐 Access Points

Once running:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 🧪 Testing

```bash
# Activate environment first
conda activate shopsight

# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific tests
pytest tests/test_api.py -v
```

## 🛠️ Common Commands

```bash
# Activate environment
conda activate shopsight

# Deactivate environment
conda deactivate

# Update dependencies
conda env update -f environment.yml --prune

# List environments
conda env list

# Check installed packages
conda list
```

## 📚 Need More Info?

- **Conda Setup**: See `CONDA_SETUP.md`
- **Full Documentation**: See `README.md`
- **API Specification**: See `../BACKEND_SPEC.md`

## 🐛 Troubleshooting

### Conda not found
```bash
# Install Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

### Ollama not running
```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Pull model
ollama pull llama3.2

# Terminal 3: Start backend
./start.sh
```

### Port 8000 already in use
```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn app.main:app --reload --port 8001
```

## 💡 Pro Tips

1. **Keep environment active**: Run `conda activate shopsight` in each new terminal
2. **Use the startup script**: `./start.sh` handles everything automatically
3. **Check health endpoint**: Visit http://localhost:8000/health to verify all services
4. **Interactive docs**: Use http://localhost:8000/docs to test API endpoints
