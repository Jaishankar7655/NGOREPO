# EC2 Instance Outputs
output "ec2_instance_id" {
  description = "The ID of the EC2 instance"
  value       = aws_instance.myweb.id
}

output "ec2_public_ip" {
  description = "The public IP of the EC2 instance"
  value       = aws_instance.myweb.public_ip
}

output "ec2_private_ip" {
  description = "The private IP of the EC2 instance"
  value       = aws_instance.myweb.private_ip
}

output "ec2_public_dns" {
  description = "The public DNS of the EC2 instance"
  value       = aws_instance.myweb.public_dns
}
