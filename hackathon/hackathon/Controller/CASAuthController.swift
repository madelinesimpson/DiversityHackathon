//
//  CASAuthController.swift
//  hackathon
//
//  Created by Ananya Jain on 3/9/24.
//

import Foundation
import UIKit

// CASAuthController.swift
class CASAuthController {
    func initiateCASLogin() {
        let casLoginURL = "https://sso.gatech.edu/cas/login"
        guard let url = URL(string: casLoginURL) else { return }
        UIApplication.shared.open(url, options: [:], completionHandler: nil)
    }

    func handleCASCallback(url: URL) {
        guard let ticket = extractTicket(from: url) else {
            
            return
        }

        // Validate the ticket with the CAS server
        validateCASTicket(ticket: ticket)
    }

    func extractTicket(from url: URL) -> String? {
        guard let components = URLComponents(url: url, resolvingAgainstBaseURL: false),
              let ticket = components.queryItems?.first(where: { $0.name == "ticket" })?.value else {
            return nil
        }
        return ticket
    }

    func validateCASTicket(ticket: String) {
        // Your code for validating CAS ticket
    }
}
