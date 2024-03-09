import SwiftUI

struct DropdownMenuSelector: View {
    @State private var selectedItemIndex = 0
    @State private var isExpanded = false
    
    let options = ["Georgia Institute of Technology", "Georgia State University", "University of Georgia", "Kennesaw State University"]
    
    var body: some View {
        VStack {
            HStack {
                Text("Select your school below").font(.custom("Futura", size:20)).foregroundColor(.white)

                Button(action: {
                    self.isExpanded.toggle()
                }) {
                    Image(systemName: "chevron.down")
                        .rotationEffect(.degrees(isExpanded ? 180 : 0))
                }
                .padding(8)
            }
            .padding(20)
            .background(Color.green.opacity(0.8))
            .cornerRadius(25)
            if isExpanded {
                ForEach(0..<options.count, id: \.self) { index in
                    Button(action: {
                        self.selectedItemIndex = index
                        self.isExpanded.toggle()
                    }) {
                        Text(self.options[index])
                            .foregroundColor(.primary)
                            .padding(8)
                            .background(index == self.selectedItemIndex ? Color.blue.opacity(0.2) : Color.clear)
                    }
                }
            }
            Text("\(options[selectedItemIndex])")
        }
        .padding()
    }
}

struct DropdownMenuSelector_Previews: PreviewProvider {
    static var previews: some View {
        DropdownMenuSelector()
    }
}
