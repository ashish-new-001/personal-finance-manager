import SwiftUI

struct AddTransactionView: View {
    @State private var amount: String = ""
    @State private var category: String = ""
    @State private var date: String = ""

    var body: some View {
        Form {
            Section(header: Text("Transaction Details")) {
                TextField("Amount", text: $amount)
                    .keyboardType(.decimalPad)
                TextField("Category", text: $category)
                TextField("Date (YYYY-MM-DD)", text: $date)
            }
            Button("Save Transaction") {
                // Handle save logic here
            }
        }
        .navigationTitle("Add Transaction")
    }
}

struct AddTransactionView_Previews: PreviewProvider {
    static var previews: some View {
        AddTransactionView()
    }
}
