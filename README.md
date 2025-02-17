# Developer Relations Engineer Assessment

This challenge was an exciting deep dive into understanding how Smart Contracts work on Algorand. At first, it seemed like a straightforward task, but as I explored further, I realized the depth and complexity of the abstractions provided by Algokit. The learning process was rewarding!

## 📌 Key Learnings

Here are the main concepts I learned throughout this challenge:

| Topic                           | Key Takeaways |
|---------------------------------|--------------|
| **Development Environment**     | Setting up and running the local sandbox. |
| **Sandbox Communication**       | Understanding how different resources interact. |
| **Algorand Core Concepts**      | Applications, Accounts, Assets, Transactions, and Wallets. |
| **Smart Contracts**             | Writing, testing, and deploying contracts with defined rules. |
| **Algokit**                     | Exploring benefits, constraints, and best practices. |
| **Lora & Goal CLI**             | Usage across LocalNet, TestNet, and MainNet. |
| **Smart Contract Testing**      | Writing test cases with `pytest` to validate execution. |
| **Deployment Strategies**       | Cost calculation, deployment, and execution flow analysis. |
| **Blockchain Workflow**         | End-to-end understanding of how contracts operate. |

Beyond these structured learnings, I also explored how to work with Boxes without relying on Algopy’s abstractions. I wanted to understand how to "manually" configure their creation and manage values, diving deeper into the mechanics of how storage works at a lower level. This gave me more control over execution and a better appreciation of the complexity behind these structures. For developers looking for more flexibility and customization, this approach is definitely worth experimenting with.

## 🔁 Learning Pathway

Below is a structured flowchart representing my learning journey through this challenge:

```
[Setup Sandbox] --> [Explore Algorand Concepts] --> [Develop Smart Contracts] --> [Test with Pytest] \
   |                                                           |                                    /
   |                                                           v                                   /
   |--> [Deploy on LocalNet] --> [Deploy on TestNet] --> [Analyze Costs & Optimization] --> [Refine & Iterate]
```

## 📸 Build & Deployment Process

### LocalNet Running
![LocalNet Running](/assets/localnet_running.png)
(That's power from ChainsawMan in the background XD)

### Wallet Created
![Wallet Created](/assets/wallet_created.png)

### Application Built Successfully
![Successfully Built](/assets/successfull_build.png)

### Application Deployed (LocalNet)
![Deployed on LocalNet](/assets/successfull_deploy.png)

### Application Deployment on Lora (LocalNet)
![Deployment on Lora](/assets/application_deployment_lora.png)

### Smart Contract Execution (LocalNet)
![Smart Contract Execution](/assets/smart_contract_working.png)

### Box Listing (Terminal - LocalNet)
![Box Listing](/assets/box_listing_for_app.png)

### Box Listing (Lora - LocalNet)
![Box on Lora](/assets/application_box_on_lora.png)

### Application Execution (TestNet)
![Application Execution TestNet](/assets/test_net_assessment_app_call.png)

### Box Listing (TestNet)
![Box Listing TestNet](/assets/test_net_app_box.png)

## 🔗  Links

- **Application Details with Boxes (TestNet):**
  [View on Lora](https://lora.algokit.io/testnet/application/733993462)

- **Application Call (TestNet):**
  [View Transaction](https://lora.algokit.io/testnet/transaction/SDXRML7KAT326H5HNBCJ6YIZBZONFZR2RKJLBQALM2VH5WNNEWGA)


## 🛠 Running Tests

To ensure the smart contract is properly built, tested, and deployed, follow these steps:

### 1️⃣ Start the Local Server
Run the local sandbox environment:
```sh
algokit localnet start
```

### 2️⃣ Create a Wallet
Generate a new wallet with a custom name:
```sh
algokit wallet new {name}
```
Important: Fund your wallet using Goal or Lora.

### 3️⃣ Build the Application (If Necessary)
If the application requires compilation, run:
```sh
algokit project run build
```

### 4️⃣ Access the project directory
```sh
cd projects/devrel_assessment
```

### 5️⃣ Run the Tests
Execute the test suite using `pytest`:
```sh
poetry run python -m pytest smart_contracts/hello_world/hello_world_test.py
```

You should see something like that:

- **Successful Tests:**
![Tests Passing](/assets/tests_passing.png)

### 6️⃣ Deploy the Application (Optional)
If you want to deploy your contract:
```sh
algokit project deploy
```


##  Final Thoughts
During development, I extensively explored **official documentation, articles, guides, and discussions on Discord**. While I gained a solid understanding, I identified some **areas for improvement** that could make the learning process more intuitive for developers.

I'll be submitting a separate document with detailed feedback along with the repository link. I also recognize that **documentation updates are already in progress**, so many of these points might be addressed soon.

This challenge was more than a technical exercise, it was an opportunity to experience how simple is to create smart contracts using algokit and to understand a lot more about how everything works. I enjoyed exploring the platform, pushing the boundaries of the available tools, and identifying areas for improvement.

---

✨ **Excited for the next steps!** 🚀

