# Contributing to Trackarbon

Thanks for considering contributing to this project! Let's dive into how to contribute to Trackarbon.

---

## 🧱 How to Contribute

### 1) 🌱 Submit a new estimation / convertion method

#### 1.1) Submission Process

- Clone the repository
  ```bash
  git clone https://github.com/fondationsahar/trackarbon-core.git
  cd trackarbon-core
  ```

- Set up the development environment with uv:
  ```bash
  # Install uv if you haven't already
  curl -LsSf https://astral.sh/uv/install.sh | sh

  # Create a virtual environment and install dependencies
  uv venv
  source .venv/bin/activate  # On Windows: .venv\Scripts\activate

  # Install the project with dev dependencies
  uv pip install -e . --group dev
  ```

- Create a new branch:
  ```bash
  git checkout -b energy/your-estimation-method-name
  ```
  if an energy estimator
  ```bash
  git checkout -b carbon/your-convertor-method-name
  ```
  if a carbon convertor method


- Submit a PR with:
  - Your new estimator located either at `src/infrastructure/estimation/energy/your_estimator_name.py` if an energy estimation method or at `src/infrastructure/estimation/carbon/your_convertor_name.py` if a new energy to carbon convertor.
  - Associated tests

#### 1.2) How to build my method

In order for the estimator to be compatible with the framework, **it needs to inherit from the associated base class**. For example, for an energy estimation method, from `BaseEnergyEstimator`. This means that the compute method takes a list of `Event` / `EventWithEnergy` objects, which define which parameters are available for the estimator.

For a quick simple example you can look at `src/infrastructure/estimation/energy/my_estimator.py` and `src/infrastructure/estimation/convertor/my_convertor.py`.

The `development_notebook.ipynb` is here to give you inspiration on how to iterate on your method.

⚠️ **If your estimator needs additional parameters** please use [GitHub Issues](https://github.com/fondationsahar/trackarbon-core/issues/new) to suggest extending the `Event` or `AIEventMetadata` classes.
