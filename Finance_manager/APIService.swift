//
//  APIService.swift
//  Finance_manager
//
//  Created by Rishika Meena on 21/12/24.
//


import Foundation

struct Transaction: Identifiable, Codable {
    var id: Int
    var amount: Double
    var category: String
    var date: String
}

class APIService {
    static let shared = APIService() // Singleton to share the instance across the app
    
    private let baseURL = "http://load-balancer-new-310376522.ap-south-1.elb.amazonaws.com/transactions"

    
    // MARK: - Fetch all transactions
    func fetchTransactions(completion: @escaping ([Transaction]?, Error?) -> Void) {
        guard let url = URL(string: baseURL) else {
            completion(nil, NSError(domain: "Invalid URL", code: 400, userInfo: nil))
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        
        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                completion(nil, error)
                return
            }
            
            do {
                let transactions = try JSONDecoder().decode([Transaction].self, from: data!)
                completion(transactions, nil)
            } catch {
                completion(nil, error)
            }
        }
        
        task.resume()
    }
    
    // MARK: - Add new transaction
    func addTransaction(transaction: Transaction, completion: @escaping (Bool, Error?) -> Void) {
        guard let url = URL(string: baseURL) else {
            completion(false, NSError(domain: "Invalid URL", code: 400, userInfo: nil))
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        do {
            let body = try JSONEncoder().encode(transaction)
            request.httpBody = body
        } catch {
            completion(false, error)
            return
        }
        
        let task = URLSession.shared.dataTask(with: request) { _, _, error in
            if let error = error {
                completion(false, error)
                return
            }
            completion(true, nil)
        }
        
        task.resume()
    }
}
