import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- CONFIGURATION ---
RESULTS_FILE = "experiment_results_detailed.csv"
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def load_and_prepare_data(file_path):
    """Loads the CSV and prepares the op_set for grouping."""
    print(f"Loading results from {file_path}...")
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    
    # Ensure op_set is a string for grouping
    df['op_set_str'] = df['op_set'].astype(str)
    
    print(f"Data loaded: {len(df)} total runs.")
    return df

def analyze_quality_and_robustness(df):
    """Step 1: Analyze Quality (Mean Final Obj) and Robustness (Std Dev)."""
    print("\n" + "="*80)
    print("🏆 Step 1: Quality (Mean Objective - Higher is Better) and Robustness (Std Dev)")
    print("="*80)
    
    quality_summary = df.groupby(['strategy', 'alpha', 'op_set_str']).agg(
        mean_obj=('final_obj', 'mean'),
        std_obj=('final_obj', 'std'),
        mean_time=('total_time', 'mean'),
        num_runs=('seed', 'count')
    ).sort_values(by='mean_obj', ascending=False)  # Maximization
    
    quality_summary['CV_obj'] = (quality_summary['std_obj'] / np.abs(quality_summary['mean_obj'])) * 100
    
    print("\n--- Summary Ranked by Mean Final Objective (Highest is Best) ---")
    print(quality_summary.head(15).round(2))
    
    print("\n--- Interpretation ---")
    best_config = quality_summary.index[0]
    print(f"The best performing configuration on average is: **{best_config}**.")
    print(f"It achieved a mean objective of **{quality_summary.iloc[0]['mean_obj']:.2f}** "
          f"with robustness (CV) of **{quality_summary.iloc[0]['CV_obj']:.2f}%**.")
    
    return quality_summary

def analyze_efficiency_and_tradeoff(df):
    """Step 2: Analyze Efficiency (Time) and Quality/Time Trade-off."""
    print("\n" + "="*80)
    print("⚡ Step 2: Efficiency (Time) and Quality/Time Trade-off")
    print("="*80)
    
    efficiency_summary = df.groupby('strategy').agg(
        mean_obj=('final_obj', 'mean'),
        mean_time=('total_time', 'mean'),
        mean_iterations=('iterations', 'mean')
    )
    
    # For maximization: obj/time (higher = better)
    efficiency_summary['performance_metric'] = efficiency_summary['mean_obj'] / efficiency_summary['mean_time']
    
    print("\n--- Strategy Efficiency Summary ---")
    print(efficiency_summary.sort_values(by='performance_metric', ascending=False).round(2))

    print("\n--- Operator Set Efficiency ---")
    op_summary = df.groupby('op_set_str').agg(
        mean_obj=('final_obj', 'mean'),
        mean_time=('total_time', 'mean'),
    ).sort_values(by='mean_time', ascending=True)
    print(op_summary.round(2))
    
    print("\n--- Interpretation ---")
    try:
        if efficiency_summary.loc['first', 'mean_time'] < efficiency_summary.loc['best', 'mean_time']:
            quality_diff = ((efficiency_summary.loc['best', 'mean_obj'] / efficiency_summary.loc['first', 'mean_obj']) - 1) * 100
            time_ratio = efficiency_summary.loc['best', 'mean_time'] / efficiency_summary.loc['first', 'mean_time']
            
            print(f"The **'first'** strategy is **{time_ratio:.1f}× faster** than 'best'.")
            print(f"It sacrifices **{quality_diff:.2f}%** in solution quality (lower objective).")
            print("Decide if the speed gain is worth the small loss in quality.")
    except KeyError:
        pass

def visualize_results(df):
    """Step 3: Visualize key comparisons for intuitive understanding."""
    print("\n" + "="*80)
    print("📈 Step 3: Visualization")
    print("="*80)
    
    df_agg = df.groupby(['strategy', 'alpha']).agg(
        mean_obj=('final_obj', 'mean'),
        mean_time=('total_time', 'mean'),
    ).reset_index()
    
    # Add performance metric for visualization
    df_agg['performance_metric'] = df_agg['mean_obj'] / df_agg['mean_time']
    
    plt.figure(figsize=(18, 6))

    # Plot 1: Mean Objective vs. Alpha by Strategy
    plt.subplot(1, 3, 1)
    sns.barplot(data=df_agg, x='alpha', y='mean_obj', hue='strategy', palette='viridis')
    plt.title('Mean Final Objective by Alpha and Strategy (Higher = Better)', fontsize=13)
    plt.xlabel('Alpha')
    plt.ylabel('Mean Objective Value')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Plot 2: Mean Time vs. Alpha by Strategy
    plt.subplot(1, 3, 2)
    sns.barplot(data=df_agg, x='alpha', y='mean_time', hue='strategy', palette='plasma')
    plt.title('Mean Total Time by Alpha and Strategy (Lower = Better)', fontsize=13)
    plt.xlabel('Alpha')
    plt.ylabel('Mean Time (s)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Plot 3: Performance Metric (Obj/Time) ranked
    plt.subplot(1, 3, 3)
    df_ranked = df_agg.sort_values(by='performance_metric', ascending=False)
    sns.barplot(data=df_ranked, x='performance_metric', y='strategy', hue='alpha', palette='coolwarm')
    plt.title('Performance Metric (Obj / Time) — Higher = Better', fontsize=13)
    plt.xlabel('Performance Metric')
    plt.ylabel('Strategy')
    plt.grid(axis='x', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()
    print("Visualization plots generated.")

def main_analysis():
    df = load_and_prepare_data(RESULTS_FILE)
    if df is None:
        return

    # 1. Quality and Robustness
    analyze_quality_and_robustness(df)
    
    # 2. Efficiency and Trade-off
    analyze_efficiency_and_tradeoff(df)
    
    # 3. Visualization
    visualize_results(df)
    
    print("\n" + "="*80)
    print("✅ Analysis Complete.")
    print("For comparison to published results, calculate the % deviation: "
          "(Your Result - Published Result) / Published Result")
    print("Use the 'mean_obj' or 'performance_metric' of the best configuration identified above.")
    print("="*80)

if __name__ == "__main__":
    main_analysis()
