


 
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
 
        # Save the latest state so the chatbot tab can answer questions about
        # it without needing any external API key.
        self.last_state = {
            "score": score, "status": status, "payment_history": payment_history,
            "utilization": utilization, "history_length": history_length,
            "new_credit": new_credit, "projected_gain": projected_gain,
            "target_score": target_score, "recommendations": recommendations,
        }
 
        return report, df, fig
 
    # ------------------------------------------------------------------
    # Rule-based chatbot — answers questions using the last computed
    # assessment. No external API key required, so it always works.
    # ------------------------------------------------------------------
    def chat_reply(self, message, history):
        state = getattr(self, "last_state", None)
        if state is None:
            return "Please run **Run Agent Assessment** on the first tab first, then come back and ask me anything about your result."
 
        msg = message.lower()
 
        if any(w in msg for w in ["util", "balance", "card"]):
            return (
                f"Your credit utilization is **{state['utilization']}%**. "
                + ("That's above the recommended 30% ceiling — paying down balances is usually "
                   "the fastest way to recover points." if state['utilization'] > 30
                   else "That's within the healthy range (under 30%) — keep it there.")
            )
 
        if any(w in msg for w in ["payment", "late", "pay"]):
            return (
                f"Your on-time payment record is **{state['payment_history']}%**. "
                + ("Even one more missed payment can undo months of progress — turning on "
                   "autopay is the highest-leverage fix here." if state['payment_history'] < 95
                   else "This is already strong — consistent on-time payments are your biggest asset.")
            )
 
        if any(w in msg for w in ["age", "history", "old", "long"]):
            return (
                f"Your credit history length is **{state['history_length']} years**. "
                + ("This is still building — avoid closing your oldest accounts, it only "
                   "improves with time." if state['history_length'] < 3
                   else "This is a solid, established history.")
            )
 
        if any(w in msg for w in ["inquiry", "inquiries", "apply", "new credit", "loan", "car"]):
            return (
                f"You have **{state['new_credit']}** hard inquiries in the last 6 months. "
                + ("That's on the high side — pausing new applications for a few months lets "
                   "these fade." if state['new_credit'] > 2
                   else "That's a reasonable, low level of recent credit-seeking.")
            )
 
        if any(w in msg for w in ["target", "gain", "improve", "increase", "raise", "projected"]):
            return (
                f"Based on your current profile, the estimated realistic ceiling is "
                f"**{state['target_score']}** (a potential gain of **+{state['projected_gain']} points** "
                f"from your current {state['score']})."
            )
 
        if any(w in msg for w in ["score", "status", "overall", "how am i", "summary"]):
            return (
                f"Your current score is **{state['score']}**, rated **{state['status']}**. "
                f"Top recommendation right now: {state['recommendations'][0] if state['recommendations'] else 'Keep up current habits.'}"
            )
 
        # Default: return the full list of recommendations
        return "Here's what I'd focus on:\n\n" + "\n".join(f"- {r}" for r in state["recommendations"])
 
 
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
 
    gr.Markdown("---")
    gr.Markdown("### 💬 Ask the Agent")
    gr.Markdown("Run an assessment above first, then ask follow-up questions — e.g. *\"How can I raise my score?\"* or *\"What about my inquiries?\"*")
    gr.ChatInterface(fn=agent.chat_reply)
 
import os

demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 10000))
)
 
