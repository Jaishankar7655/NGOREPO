# AMI ID for EC2
variable "ami_id" {
  description = "The AMI ID for the EC2 instance"
  type        = string
  default     = "ami-02d26659fd82cf299"
}

# Instance type for EC2
variable "instance_type" {
  description = "The type of EC2 instance to launch"
  type        = string
  default     = "t3.medium"
}

# EC2 Root Volume Size
variable "root_volume_size" {
  description = "The size of the root volume in GB"
  type        = number
  default     = 30
}

# EC2 Root Volume Type
variable "root_volume_type" {
  description = "The type of root volume (gp2/gp3/io1)"
  type        = string
  default     = "gp3"
}

# EC2 Instance Name Tag
variable "instance_name" {
  description = "Tag for the EC2 instance"
  type        = string
  default     = "my-web-server"
}
