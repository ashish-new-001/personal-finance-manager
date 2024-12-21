import SwiftUI

struct AddTransactionView: View {
    @State private var amount: String = ""
    @State private var category: String = ""
    @State private var date: String = ""
    
    @Environment(\.presentationMode) var presentationMode

    var body: some View {
        Form {
            Section(header: Text("Transaction Details")) {
                TextField("Amount", text: $amount)
                    .keyboardType(.decimalPad)
                TextField("Category", text: $category)
                TextField("Date (YYYY-MM-DD)", text: $date)
            }
            Button("Save Transaction") {
                let newTransaction = Transaction(id: 0, amount: Double(amount) ?? 0.0, category: category, date: date)
                
                APIService.shared.addTransaction(transaction: newTransaction) { success, error in
                    if success {
                        self.presentationMode.wrappedValue.dismiss()
                    } else {
                        print("Error adding transaction: \(error?.localizedDescription ?? "Unknown error")")
                    }
                }
            }
        }
        .navigationTitle("Add Transaction")
    }
}
