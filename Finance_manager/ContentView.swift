import SwiftUI

struct ContentView: View {
    @State private var transactions: [Transaction] = []
    
    var body: some View {
        NavigationView {
            List(transactions) { transaction in
                VStack(alignment: .leading) {
                    Text("Category: \(transaction.category)")
                        .font(.headline)
                    Text("Amount: $\(transaction.amount, specifier: "%.2f")")
                    Text("Date: \(transaction.date)")
                        .font(.subheadline)
                        .foregroundColor(.gray)
                }
            }
            .onAppear {
                APIService.shared.fetchTransactions { transactions, error in
                    if let transactions = transactions {
                        self.transactions = transactions
                    } else {
                        print("Error fetching transactions: \(error?.localizedDescription ?? "Unknown error")")
                    }
                }
            }
            .navigationTitle("Transactions")
            .navigationBarItems(trailing: NavigationLink(destination: AddTransactionView()) {
                Text("Add Transaction")
                    .foregroundColor(.blue)
            })
        }
    }
}
