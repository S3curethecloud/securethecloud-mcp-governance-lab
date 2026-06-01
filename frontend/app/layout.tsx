export const metadata = {
  title: "SecureTheCloud MCP Governance Lab",
  description: "Governed MCP access, policy, approval, and evidence lab platform"
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
