import tkinter as tk
from tkinter import ttk, messagebox
from textblob import TextBlob
import matplotlib.pyplot as plt
from collections import Counter


class SentimentAnalyzerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sentiment Analyzer")
        self.sentences = []
        self.sentiments = []

        self.configure(bg="#f0f0f0")
        self.create_widgets()

    def create_widgets(self):
        self.sentences_entry = tk.Text(self, height=5, width=50, wrap=tk.WORD, bg="white", fg="black",
                                       font=("Arial", 12))
        self.sentences_entry.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

        self.method_label = tk.Label(self, text="Sentiment Analysis Method:", bg="#f0f0f0", fg="black",
                                     font=("Arial", 12))
        self.method_label.grid(row=1, column=0, padx=10, pady=5)
        self.method_var = tk.StringVar(value="TextBlob")
        self.method_dropdown = ttk.Combobox(self, textvariable=self.method_var, values=["TextBlob", "Custom"], width=15)
        self.method_dropdown.grid(row=1, column=1, padx=10, pady=5)

        self.analyze_button = tk.Button(self, text="Analyze", command=self.analyze_sentiment, bg="#4CAF50", fg="white",
                                        font=("Arial", 12, "bold"))
        self.analyze_button.grid(row=1, column=2, padx=10, pady=5)

        self.results_label = tk.Label(self, text="Sentiment Analysis Results:", bg="#f0f0f0", fg="black",
                                      font=("Arial", 12, "bold"))
        self.results_label.grid(row=2, column=0, padx=10, pady=5, columnspan=3)

        self.results_text = tk.Text(self, height=10, width=50, wrap=tk.WORD, bg="white", fg="black", font=("Arial", 12))
        self.results_text.grid(row=3, column=0, padx=10, pady=5, columnspan=3)

        self.history_label = tk.Label(self, text="Sentiment History:", bg="#f0f0f0", fg="black",
                                      font=("Arial", 12, "bold"))
        self.history_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
        self.history_text = tk.Text(self, height=5, width=50, wrap=tk.WORD, bg="white", fg="black", font=("Arial", 12))
        self.history_text.grid(row=5, column=0, padx=10, pady=5, columnspan=3)

        self.visualize_button = tk.Button(self, text="Visualize", command=self.visualize_sentiments, bg="#008CBA",
                                          fg="white", font=("Arial", 12, "bold"))
        self.visualize_button.grid(row=6, column=0, padx=10, pady=10, columnspan=3)

    def analyze_sentiment(self):
        sentences = self.sentences_entry.get("1.0", tk.END).strip().split("\n")
        method = self.method_var.get()

        for sentence in sentences:
            try:
                if method == "TextBlob":
                    blob = TextBlob(sentence)
                    sentiment = blob.sentiment.polarity
                elif method == "Custom":
                    sentiment = 0.0  

                self.sentences.append(sentence)
                self.sentiments.append(sentiment)
                self.display_result(sentence, sentiment)

            except Exception as e:
                self.display_result(sentence, "Error")

        self.display_history()

    def display_result(self, sentence, sentiment):
        if isinstance(sentiment, float):
            sentiment_str = "Positive" if sentiment > 0 else "Neutral" if sentiment == 0 else "Negative"
            sentiment_color = "#4CAF50" if sentiment_str == "Positive" else "#FF5733" if sentiment_str == "Neutral" else "#FF5733"
        else:
            sentiment_str = "Error"
            sentiment_color = "#FF5733"

        self.results_text.config(state=tk.NORMAL)
        self.results_text.insert(tk.END, f"Sentence: {sentence}\nSentiment: {sentiment_str}\n\n")
        self.results_text.tag_configure(sentiment_str, foreground=sentiment_color)
        self.results_text.insert(tk.END, "\n", sentiment_str)
        self.results_text.config(state=tk.DISABLED)

    def display_history(self):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete("1.0", tk.END)
        for i, (sentence, sentiment) in enumerate(zip(self.sentences, self.sentiments), start=1):
            self.history_text.insert(tk.END, f"{i}. Sentence: {sentence}\n   Sentiment: {sentiment:.2f}\n\n")
        self.history_text.config(state=tk.DISABLED)

    def visualize_sentiments(self):
        if not self.sentiments:
            messagebox.showerror("Error", "No sentiments to visualize!")
            return

        sentiments = [sentiment for sentiment in self.sentiments if isinstance(sentiment, float)]
        sentiment_counts = Counter(sentiments)
        labels = sentiment_counts.keys()
        sizes = sentiment_counts.values()
        colors = ["#4CAF50", "#FF5733", "#008CBA"]

        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=140)
        plt.axis("equal")
        plt.show()


if __name__ == "__main__":
    app = SentimentAnalyzerApp()
    app.mainloop()
