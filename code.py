!pip install -q gradio pandas matplotlib numpy

import gradio as gr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class EnhancedCreditAgent:
    """Enhanced AI Agent for credit optimization with visual plotting and structured analysis."""

    def analyze_profile(self, score, payment_history, utilization, history_length, new_credit):
        agent_logs = []
        recommendations = []

        # 1. Evaluate Core Status
        if score >= 750:
            status = "Excellent"
            rec_main = "Prime score status. Focus on maintaining low utilization to preserve high-tier interest rates."
        elif score >= 700:
            status = "Good"
            rec_main = "Solid financial profile. Targeted reductions in card balances will unlock prime tiers."
        elif score >= 650:
            status = "Fair"
            rec_main = "Average rating. Prioritize payment discipline and balance reductions to recover points."
        else:
            status = "Poor"
            rec_main = "Critical status. Immediate action is needed to resolve delinquent factors and manage balances."

        agent_logs.append(f"LOG: Classified base score {score} into '{status}' tier.")

        # 2. Rule Engine & Specific Interventions
        if utilization > 30:
            recommendations.append(f"⚠️ High Utilization ({utilization}%): Lower total card balances below 30% to avoid score penalties.")
            agent_logs.append(f"LOG: High utilization penalty detected ({utilization}% > 30%).")
        else:
            recommendations.append(f"✅ Healthy Utilization ({utilization}%): Maintaining balances below 30% reinforces your credit base.")
            agent_logs.append(f"LOG: Utilization check passed ({utilization}%).")

        if payment_history < 95:
            recommendations.append(f"⚠️ Payment History ({payment_history}%): Enable auto-pay. Recent late payments heavily weigh down your profile.")
            agent_logs.append(f"LOG: Payment delinquency flag triggered ({payment_history}% < 95%).")
        else:
            recommendations.append(f"✅ Strong Payment History ({payment_history}%): Consistent on-time payments are strengthening your score.")
            agent_logs.append(f"LOG: Payment record verified as healthy ({payment_history}%).")

        if history_length < 3:
            recommendations.append(f"⚠️ Short Credit Age ({history_length} yrs): Keep older lines open to extend your average credit age over time.")
            agent_logs.append(f"LOG: Credit age flagged as maturing ({history_length} yrs < 3 yrs).")

        if new_credit > 2:
            recommendations.append(f"⚠️ Frequent Inquiries ({new_credit} in 6 mos): Pause new credit applications to clear hard inquiries.")
            agent_logs.append(f"LOG: Inquiry velocity warning triggered ({new_credit} > 2).")

        # 3. Dynamic Point Projection Logic
        projected_gain = 0
        if utilization > 30: projected_gain += 25
        if payment_history < 100: projected_gain += 35
        if new_credit > 2: projected_gain += 15

        target_score = min(850, score + projected_gain)
        agent_logs.append(f"LOG: Calculated maximum potential recovery of +{projected_gain} pts. Target: {target_score}.")

        # 4. Generate Pandas Structural Table
        df = pd.DataFrame({
            "Credit Parameter": ["Credit Score", "Payment Record", "Utilization Rate", "Credit History Age", "Hard Inquiries"],
            "Current Profile": [f"{score}", f"{payment_history}%", f"{utilization}%", f"{history_length} Years", f"{new_credit}"],
            "Optimal Benchmark": ["750+", "95%+", "< 30%", "3+ Years", "< 2"],
            "Parameter Status": [
                status,
                "Optimal" if payment_history >= 95 else "Needs Attention",
                "Optimal" if utilization <= 30 else "Needs Attention",
                "Optimal" if history_length >= 3 else "Building Age",
                "Optimal" if new_credit <= 2 else "Too High"
            ]
        })

        # 5. Render Matplotlib Forecast Plot
        fig, ax = plt.subplots(figsize=(6, 3))
        categories = ['Current', 'Potential Gain', 'Target Score']
        values = [score, projected_gain, target_score]
        bar_colors = ['#2b5c8f', '#27ae60', '#8e44ad']

        bars = ax.bar(categories, values, color=bar_colors, width=0.45)
        ax.set_ylim(0, 950)
        ax.set_ylabel("Credit Score Points")
        ax.set_title("Forecasted Score Trajectory", fontsize=11, fontweight='bold')

        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontweight='bold')

        plt.tight_layout()

        # 6. Structure Final Markdown Report
        report = f"### Overall Assessment: **{status}** ({score} Points)\n"
        report += f"**Core Advice:** {rec_main}\n\n"
        report += f"**Projected Score Growth:** +{projected_gain} Points (Target Score: **{target_score}**)\n\n"
        report += "### Actionable Steps:\n" + "\n".join([f"- {r}" for r in recommendations]) + "\n\n"
        report += "### Agent Execution Logs:\n" + "\n".join([f"`{log}`" for log in agent_logs])

        return report, df, fig

agent = EnhancedCreditAgent()

# --- Gradio UI Setup ---
with gr.Blocks(title="AI Credit Score Guidance Agent") as demo:
    gr.Markdown("# 💳 AI Credit Score Guidance Agent")
    gr.Markdown("Adjust your financial profile parameters to trigger the AI agent's analysis, metric comparison, and visualization engine.")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Input Financial Parameters")
            score_in = gr.Slider(300, 850, value=670, step=1, label="Current Credit Score")
            pay_in = gr.Slider(50, 100, value=92, step=1, label="On-time Payment Record (%)")
            util_in = gr.Slider(0, 100, value=45, step=1, label="Credit Utilization Ratio (%)")
            age_in = gr.Slider(0, 20, value=2, step=0.5, label="Credit History Length (Years)")
            inq_in = gr.Number(value=3, label="Hard Inquiries (Last 6 Months)")
            btn = gr.Button("Run Agent Assessment", variant="primary")

        with gr.Column(scale=1):
            out_summary = gr.Markdown(label="Agent Analysis & Guidance")
            out_plot = gr.Plot(label="Score Trajectory Chart")
            out_df = gr.Dataframe(label="Detailed Metric Breakdown")

    btn.click(
        fn=agent.analyze_profile,
        inputs=[score_in, pay_in, util_in, age_in, inq_in],
        outputs=[out_summary, out_df, out_plot]
    )

demo.launch(share=True, debug=True)
