import pandas as pd
import matplotlib.pyplot as plt
import os

# =====================================================
# FILE PATHS
# =====================================================

BEFORE_FILE = r"E:\LLM_prompt_inj_lab\logs\before_defense.csv"
AFTER_FILE = r"E:\LLM_prompt_inj_lab\logs\after_defense.csv"

SUMMARY_FILE = "logs/summary_report.txt"
DEFENSE_REPORT = "logs/defense_report.txt"

ASR_GRAPH = "logs/asr_comparison.png"
LEAK_GRAPH = "logs/leak_comparison.png"

# =====================================================
# CHECK FILES
# =====================================================

if not os.path.exists(BEFORE_FILE):
    print(f"Missing file: {BEFORE_FILE}")
    exit()

if not os.path.exists(AFTER_FILE):
    print(f"Missing file: {AFTER_FILE}")
    exit()

# =====================================================
# LOAD DATA
# =====================================================

before_df = pd.read_csv(BEFORE_FILE)
after_df = pd.read_csv(AFTER_FILE)

print("\nDatasets Loaded Successfully\n")

# =====================================================
# METRIC FUNCTION
# =====================================================

def calculate_metrics(df):

    total_tests = len(df)

    no_leak = len(
        df[df["Classification"] == "No Leak"]
    )

    partial_leak = len(
        df[df["Classification"] == "Partial Leak"]
    )

    full_leak = len(
        df[df["Classification"] == "Full Leak"]
    )

    blocked = 0

    if "Blocked" in df["Classification"].values:

        blocked = len(
            df[df["Classification"] == "Blocked"]
        )

    successful_attacks = (
        partial_leak +
        full_leak
    )

    if total_tests > 0:

        asr = (
            successful_attacks /
            total_tests
        ) * 100

        avg_leak_score = (
            df["Leak Score"].mean()
        )

    else:

        asr = 0
        avg_leak_score = 0

    return {
        "total": total_tests,
        "no_leak": no_leak,
        "partial": partial_leak,
        "full": full_leak,
        "blocked": blocked,
        "successful": successful_attacks,
        "asr": asr,
        "avg_score": avg_leak_score
    }

# =====================================================
# CALCULATE
# =====================================================

before = calculate_metrics(before_df)
after = calculate_metrics(after_df)

# =====================================================
# DEFENSE EFFECTIVENESS
# =====================================================

if before["asr"] > 0:

    defense_effectiveness = (
        (
            before["asr"] -
            after["asr"]
        )
        /
        before["asr"]
    ) * 100

else:

    defense_effectiveness = 0

# =====================================================
# DISPLAY RESULTS
# =====================================================

print("=" * 70)
print("PROMPT INJECTION DEFENSE ANALYSIS")
print("=" * 70)

print("\nBEFORE DEFENSE")
print("------------------------")

print(f"Total Tests        : {before['total']}")
print(f"No Leak            : {before['no_leak']}")
print(f"Partial Leak       : {before['partial']}")
print(f"Full Leak          : {before['full']}")
print(f"ASR                : {before['asr']:.2f}%")

print("\nAFTER DEFENSE")
print("------------------------")

print(f"Total Tests        : {after['total']}")
print(f"No Leak            : {after['no_leak']}")
print(f"Partial Leak       : {after['partial']}")
print(f"Full Leak          : {after['full']}")
print(f"Blocked Requests   : {after['blocked']}")
print(f"ASR                : {after['asr']:.2f}%")

print("\nDEFENSE EFFECTIVENESS")
print("------------------------")

print(
    f"Reduction in ASR : "
    f"{defense_effectiveness:.2f}%"
)

# =====================================================
# ASR COMPARISON GRAPH
# =====================================================

plt.figure(figsize=(8, 5))

plt.bar(
    ["Before Defense", "After Defense"],
    [
        before["asr"],
        after["asr"]
    ]
)

plt.title("Attack Success Rate Comparison")
plt.ylabel("ASR (%)")

plt.tight_layout()

plt.savefig(ASR_GRAPH)

plt.close()

print(f"\nSaved: {ASR_GRAPH}")

# =====================================================
# LEAK COMPARISON GRAPH
# =====================================================

categories = [
    "No Leak",
    "Partial Leak",
    "Full Leak"
]

before_counts = [
    before["no_leak"],
    before["partial"],
    before["full"]
]

after_counts = [
    after["no_leak"],
    after["partial"],
    after["full"]
]

x = range(len(categories))

plt.figure(figsize=(8, 5))

plt.bar(
    [i - 0.2 for i in x],
    before_counts,
    width=0.4,
    label="Before"
)

plt.bar(
    [i + 0.2 for i in x],
    after_counts,
    width=0.4,
    label="After"
)

plt.xticks(x, categories)

plt.title("Leak Classification Comparison")

plt.ylabel("Count")

plt.legend()

plt.tight_layout()

plt.savefig(LEAK_GRAPH)

plt.close()

print(f"Saved: {LEAK_GRAPH}")

# =====================================================
# SUMMARY REPORT
# =====================================================

with open(
    SUMMARY_FILE,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "PROMPT INJECTION ANALYSIS REPORT\n"
    )

    f.write("=" * 60 + "\n\n")

    f.write("BEFORE DEFENSE\n")
    f.write("--------------------\n")

    f.write(
        f"Total Tests: "
        f"{before['total']}\n"
    )

    f.write(
        f"ASR: "
        f"{before['asr']:.2f}%\n"
    )

    f.write(
        f"Average Leak Score: "
        f"{before['avg_score']:.2f}\n\n"
    )

    f.write("AFTER DEFENSE\n")
    f.write("--------------------\n")

    f.write(
        f"Total Tests: "
        f"{after['total']}\n"
    )

    f.write(
        f"ASR: "
        f"{after['asr']:.2f}%\n"
    )

    f.write(
        f"Average Leak Score: "
        f"{after['avg_score']:.2f}\n\n"
    )

    f.write("DEFENSE EFFECTIVENESS\n")
    f.write("--------------------\n")

    f.write(
        f"ASR Reduction: "
        f"{defense_effectiveness:.2f}%\n"
    )

# =====================================================
# IEEE REPORT TEXT
# =====================================================

with open(
    DEFENSE_REPORT,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "The baseline system exhibited "
        f"an Attack Success Rate (ASR) "
        f"of {before['asr']:.2f}%.\n\n"
    )

    f.write(
        "After implementing layered "
        "defenses including input "
        "filtering, output filtering, "
        "prompt hardening and request "
        "monitoring, the ASR reduced "
        f"to {after['asr']:.2f}%.\n\n"
    )

    f.write(
        "The defense mechanisms achieved "
        f"an ASR reduction of "
        f"{defense_effectiveness:.2f}%."
    )

print(f"Saved: {SUMMARY_FILE}")
print(f"Saved: {DEFENSE_REPORT}")

print("\nAnalysis Completed Successfully.")