# AWS Diagram-as-Code (awsdac) Agent Instructions

## Overview

AWS Diagram-as-Code (awsdac) is a command-line tool that generates AWS infrastructure diagrams from YAML code. It allows you to create professional AWS architecture diagrams programmatically without relying on GUI tools or image libraries.

## Key Concepts

### 1. DAC File Structure
Every awsdac input file must follow this YAML structure:

```yaml
Diagram:
  DefinitionFiles:  # Required: Specifies icon definitions
    - Type: URL
      Url: "https://raw.githubusercontent.com/awslabs/diagram-as-code/main/definitions/definition-for-aws-icons-light.yaml"
  Resources:        # Required: Defines AWS resources and their relationships
    Canvas:
      Type: AWS::Diagram::Canvas
      Direction: vertical
      Children:
        - AWSCloud
  Links:            # Optional: Defines connections between resources
    - Source: Resource1
      SourcePosition: S
      Target: Resource2
      TargetPosition: N
```

### 2. Required Components

#### Canvas (Mandatory)
- **Type**: `AWS::Diagram::Canvas`
- **Purpose**: Root container for all resources
- **Requirements**: Must be exactly one Canvas resource
- **Children**: All top-level resources must be listed here

#### DefinitionFiles (Mandatory)
- **Purpose**: Provides icon definitions for AWS resources
- **Standard URL**: Use the official AWS icons definition file
- **Types**: URL, LocalFile, or Embed

## Understanding Presets

### What are Presets?

Presets are predefined styling configurations that override the default appearance of resources. They provide:
- **Consistent Styling**: Standardized colors, borders, and icons
- **Semantic Meaning**: Visual distinction between different resource types
- **Professional Appearance**: AWS-compliant design patterns

### How Presets Work

Presets are defined in the definition file with `Type: Preset` and contain:
- **Icon**: Specific AWS icon image
- **Label**: Default title and color
- **Border**: Border style and color
- **Fill**: Background color

### When to Use Presets

Use presets when you want to:
1. **Override Default Styling**: Change from generic to specific AWS service appearance
2. **Add Semantic Meaning**: Distinguish between public/private subnets, different user types, etc.
3. **Ensure Consistency**: Use standardized AWS icons and colors
4. **Improve Readability**: Make diagrams more professional and clear

### How to Use Presets

```yaml
# Basic preset usage
ResourceName:
  Type: AWS::EC2::Subnet
  Preset: PublicSubnet    # Applies public subnet styling

# Preset with custom title (overrides preset title)
ResourceName:
  Type: AWS::EC2::Subnet
  Preset: PublicSubnet
  Title: "My Custom Subnet"  # Overrides "Public Subnet" from preset

# Preset with additional properties
ResourceName:
  Type: AWS::ElasticLoadBalancingV2::LoadBalancer
  Preset: Application Load Balancer
  Direction: vertical
  Children:
    - BackendService
```

### Common Preset Categories

#### Network Presets
- `PublicSubnet` - Green border, public subnet icon
- `PrivateSubnet` - Teal border, private subnet icon
- `VPC` - Purple border, VPC icon

#### Load Balancer Presets
- `Application Load Balancer` - ALB icon and styling
- `Network Load Balancer` - NLB icon and styling
- `Classic Load Balancer` - CLB icon and styling

#### User/Identity Presets
- `User` - Single user icon
- `Users` - Multiple users icon
- `Authenticated user` - User with authentication symbol

#### Container Presets
- `AWSCloudNoLogo` - Clean AWS cloud boundary
- `Generic group` - Dashed border for logical grouping

### How Agents Can Identify Correct Presets

#### 1. Check the Definition File
The official definition file contains all available presets. Look for entries with `Type: Preset`:

```yaml
"PublicSubnet":
  Type: Preset
  Icon:
    Source: ArchitectureIconsPptxMedia
    Path: "image29.png"
  Label:
    Title: "Public Subnet"
    Color: "rgba(0, 0, 0, 255)"
  Border:
    Color: "rgba(122, 161, 22, 255)"
```

#### 2. Use Common Naming Patterns
Presets typically follow these naming conventions:
- **Service + Type**: `Application Load Balancer`, `Network Load Balancer`
- **Resource + State**: `PublicSubnet`, `PrivateSubnet`
- **Generic Terms**: `User`, `Users`, `Generic group`
- **AWS Branding**: `AWSCloudNoLogo`

#### 3. Reference Examples
Study working examples to see preset usage:
```yaml
# From examples/alb-ec2.yaml
VPCPublicSubnet1:
  Type: AWS::EC2::Subnet
  Preset: PublicSubnet    # ✅ Correct preset

ALB:
  Type: AWS::ElasticLoadBalancingV2::LoadBalancer
  Preset: Application Load Balancer    # ✅ Correct preset

User:
  Type: AWS::Diagram::Resource
  Preset: User    # ✅ Correct preset
```

#### 4. Avoid Common Mistakes
- **Don't guess**: If unsure, use the resource type without preset
- **Check spelling**: Preset names are case-sensitive
- **Use exact names**: "Application Load Balancer" not "ALB" or "Application Load Balancer"
- **Verify existence**: Only use presets that exist in the definition file

#### 5. Fallback Strategy
If a preset doesn't exist:
```yaml
# Instead of guessing a preset
ResourceName:
  Type: AWS::EC2::Subnet
  Preset: NonExistentPreset  # ❌ Will cause errors

# Use the resource type directly
ResourceName:
  Type: AWS::EC2::Subnet     # ✅ Will use default styling
  Title: "My Subnet"         # ✅ Add custom title if needed
```

### Preset vs Resource Type

#### When to Use Resource Type Only
```yaml
# Use resource type when:
# 1. No specific preset exists
# 2. You want default styling
# 3. You'll customize appearance manually

MySubnet:
  Type: AWS::EC2::Subnet
  Title: "Custom Subnet"
  BorderColor: "rgba(255,0,0,255)"  # Custom red border
```

#### When to Use Preset
```yaml
# Use preset when:
# 1. Standard AWS styling is desired
# 2. Semantic meaning is important
# 3. Consistency across diagrams

PublicSubnet:
  Type: AWS::EC2::Subnet
  Preset: PublicSubnet  # Applies standard green border and icon
```

### Preset Override Behavior

Presets can be overridden by explicit properties:
```yaml
MySubnet:
  Type: AWS::EC2::Subnet
  Preset: PublicSubnet
  Title: "Custom Name"           # Overrides preset title
  BorderColor: "rgba(255,0,0,255)"  # Overrides preset border color
  FillColor: "rgba(255,255,0,255)"  # Adds custom fill color
```

## Resource Types and Hierarchy

### 1. Container Resources
These organize and group other resources:

#### AWS::Diagram::Canvas
- **Purpose**: Root container (required)
- **Direction**: vertical/horizontal
- **Children**: Top-level resources

#### AWS::Diagram::Cloud
- **Purpose**: Represents AWS cloud boundary
- **Preset**: AWSCloudNoLogo (recommended)
- **Children**: AWS resources

#### AWS::Diagram::Region
- **Purpose**: Groups resources by AWS region
- **Title**: Region name (e.g., "us-east-1")
- **Children**: VPCs and other regional resources

#### AWS::Diagram::Account
- **Purpose**: Groups resources by AWS account
- **Title**: Account name/description
- **Children**: Regions or VPCs

### 2. Layout Resources
These control positioning and arrangement:

#### AWS::Diagram::VerticalStack
- **Purpose**: Stacks children vertically
- **Align**: left/center/right
- **Use case**: Organizing resources in columns

#### AWS::Diagram::HorizontalStack
- **Purpose**: Stacks children horizontally
- **Align**: top/center/bottom
- **Use case**: Organizing resources in rows

### 3. AWS Resources
These represent actual AWS services:

#### Network Resources
- `AWS::EC2::VPC` - Virtual Private Cloud
- `AWS::EC2::Subnet` - Subnets (use Preset: PublicSubnet/PrivateSubnet)
- `AWS::EC2::InternetGateway` - Internet Gateway
- `AWS::EC2::NatGateway` - NAT Gateway
- `AWS::EC2::TransitGateway` - Transit Gateway

#### Compute Resources
- `AWS::EC2::Instance` - EC2 instances
- `AWS::AutoScaling::AutoScalingGroup` - Auto Scaling Groups
- `AWS::ElasticLoadBalancingV2::LoadBalancer` - Load Balancers

#### Database Resources
- `AWS::RDS::DBInstance` - RDS instances
- `AWS::DirectoryService::MicrosoftAD` - Managed Directory Service

#### Generic Resources
- `AWS::Diagram::Resource` - Custom/generic resources
- `AWS::Diagram::DataCenter` - On-premises data center

## Resource Properties

### Common Properties
```yaml
ResourceName:
  Type: AWS::EC2::VPC
  Title: "My VPC"                    # Display name
  Direction: "vertical"              # vertical/horizontal
  Preset: "PublicSubnet"            # Predefined styling
  Align: "center"                   # Alignment within parent
  FillColor: "rgba(255,255,255,255)" # Background color
  BorderColor: "rgba(0,0,0,255)"    # Border color
  Children:                         # Child resources
    - ChildResource1
    - ChildResource2
  BorderChildren:                   # Resources on border
    - Position: S
      Resource: IGW
```

### Icon Fill Properties
```yaml
ResourceName:
  Type: AWS::EC2::InternetGateway
  IconFill:
    Type: rect                      # rect/none
    Color: "rgba(255,255,255,255)"  # Fill color
```

## Links and Connections

### Basic Link Structure
```yaml
Links:
  - Source: Resource1              # Source resource name
    SourcePosition: S              # Source position (16-wind rose)
    Target: Resource2              # Target resource name
    TargetPosition: N              # Target position (16-wind rose)
    TargetArrowHead:               # Arrow at target
      Type: Open                   # Open/Default
      Width: Default               # Narrow/Default/Wide
      Length: 2                    # Arrow length
```

### Link Types
#### Straight Links
```yaml
- Source: ALB
  SourcePosition: S
  Target: EC2Instance
  TargetPosition: N
  TargetArrowHead:
    Type: Open
```

#### Orthogonal Links
```yaml
- Source: Lambda
  SourcePosition: E
  Target: S3Bucket
  TargetPosition: W
  Type: orthogonal                 # Creates right-angled connections
  TargetArrowHead:
    Type: Open
```

### Link Styling
```yaml
- Source: Resource1
  SourcePosition: S
  Target: Resource2
  TargetPosition: N
  LineWidth: 3                     # Line thickness
  LineColor: "rgba(255,0,0,255)"   # Line color (red)
  LineStyle: "dashed"              # normal/dashed
```

### Link Labels
```yaml
- Source: Resource1
  SourcePosition: S
  Target: Resource2
  TargetPosition: N
  Labels:
    SourceRight:                   # Label on source right
      Title: "Data Flow"
      Color: "rgba(0,0,255,255)"   # Blue text
    TargetLeft:                    # Label on target left
      Title: "Response"
```

## Position System (16-Wind Rose)

Use these positions for SourcePosition and TargetPosition:
- **Cardinal**: N, S, E, W
- **Intercardinal**: NE, NW, SE, SW
- **Secondary**: NNE, NNW, ENE, ESE, SSE, SSW, WNW, WSW

## Common Patterns

### 1. Basic VPC with Public/Private Subnets
```yaml
VPC:
  Type: AWS::EC2::VPC
  Direction: vertical
  Children:
    - PublicSubnetStack
    - PrivateSubnetStack

PublicSubnetStack:
  Type: AWS::Diagram::HorizontalStack
  Children:
    - PublicSubnet1
    - PublicSubnet2

PrivateSubnetStack:
  Type: AWS::Diagram::HorizontalStack
  Children:
    - PrivateSubnet1
    - PrivateSubnet2

PublicSubnet1:
  Type: AWS::EC2::Subnet
  Preset: PublicSubnet
  Children:
    - EC2Instance1

PrivateSubnet1:
  Type: AWS::EC2::Subnet
  Preset: PrivateSubnet
  Children:
    - EC2Instance2
```

### 2. Multi-Region Architecture
```yaml
Regions:
  Type: AWS::Diagram::HorizontalStack
  Children:
    - Region1
    - Region2

Region1:
  Type: AWS::Region
  Title: "us-east-1"
  Direction: vertical
  Children:
    - VPC1

Region2:
  Type: AWS::Region
  Title: "us-west-2"
  Direction: vertical
  Children:
    - VPC2
```

### 3. Hybrid Architecture (On-prem + AWS)
```yaml
Canvas:
  Type: AWS::Diagram::Canvas
  Direction: vertical
  Children:
    - DataCenter
    - AWSCloud

DataCenter:
  Type: AWS::Diagram::DataCenter
  Title: "Corporate Data Center"
  Children:
    - AppServer

AWSCloud:
  Type: AWS::Diagram::Cloud
  Preset: AWSCloudNoLogo
  Children:
    - VPC
```

## Best Practices

### 1. Resource Naming
- Use descriptive, unique names
- Include region/account context when needed
- Use consistent naming conventions

### 2. Hierarchy Design
- Start with Canvas as root
- Use Cloud to represent AWS boundary
- Group related resources logically
- Use stacks for parallel resources

### 3. Link Positioning
- Use appropriate wind rose positions
- Avoid overlapping links
- Use orthogonal links for complex layouts
- Add labels for clarity

### 4. Styling
- Use presets for consistent appearance
- Apply appropriate colors for different resource types
- Use dashed lines for logical connections
- Use solid lines for physical connections

### 5. Preset Usage
- Use presets for standard AWS services
- Verify preset names in definition file
- Override preset properties when needed
- Don't guess preset names

## Command Usage

### Basic Usage
```bash
# Generate diagram from YAML file
awsdac input.yaml

# Specify output file
awsdac input.yaml -o diagram.png

# Enable verbose logging
awsdac input.yaml -v
```

### CloudFormation Integration (Beta)
```bash
# Generate diagram from CloudFormation template
awsdac template.yaml --cfn-template

# Generate DAC file from CloudFormation template
awsdac template.yaml --cfn-template --dac-file
```

## Common Mistakes to Avoid

1. **Missing Canvas**: Every diagram must have exactly one Canvas resource
2. **Invalid Resource References**: All Children and Links must reference existing resources
3. **Circular Dependencies**: Avoid circular parent-child relationships
4. **Invalid Positions**: Use valid 16-wind rose positions only
5. **Missing DefinitionFiles**: Always include the AWS icons definition file
6. **Invalid Presets**: Only use presets that exist in the definition file
7. **Case Sensitivity**: Preset names are case-sensitive

## Troubleshooting

### Common Issues
1. **Resource not found**: Check spelling and ensure resource exists
2. **Invalid YAML**: Validate YAML syntax
3. **Missing icons**: Ensure DefinitionFiles URL is accessible
4. **Layout issues**: Adjust Direction and Align properties
5. **Preset not found**: Verify preset name in definition file

### Debug Tips
- Use `-v` flag for verbose output
- Check resource hierarchy in Children arrays
- Verify all referenced resources exist
- Test with simple examples first
- Check preset names against definition file

## Example Templates

### Simple ALB + EC2
```yaml
Diagram:
  DefinitionFiles:
    - Type: URL
      Url: "https://raw.githubusercontent.com/awslabs/diagram-as-code/main/definitions/definition-for-aws-icons-light.yaml"
  Resources:
    Canvas:
      Type: AWS::Diagram::Canvas
      Direction: vertical
      Children:
        - AWSCloud
        - User
    AWSCloud:
      Type: AWS::Diagram::Cloud
      Preset: AWSCloudNoLogo
      Direction: vertical
      Children:
        - VPC
    VPC:
      Type: AWS::EC2::VPC
      Direction: vertical
      Children:
        - SubnetStack
        - ALB
    SubnetStack:
      Type: AWS::Diagram::HorizontalStack
      Children:
        - Subnet1
        - Subnet2
    Subnet1:
      Type: AWS::EC2::Subnet
      Preset: PublicSubnet
      Children:
        - EC2Instance1
    Subnet2:
      Type: AWS::EC2::Subnet
      Preset: PublicSubnet
      Children:
        - EC2Instance2
    ALB:
      Type: AWS::ElasticLoadBalancingV2::LoadBalancer
      Preset: Application Load Balancer
    EC2Instance1:
      Type: AWS::EC2::Instance
    EC2Instance2:
      Type: AWS::EC2::Instance
    User:
      Type: AWS::Diagram::Resource
      Preset: User
  Links:
    - Source: ALB
      SourcePosition: S
      Target: EC2Instance1
      TargetPosition: N
      TargetArrowHead:
        Type: Open
    - Source: ALB
      SourcePosition: S
      Target: EC2Instance2
      TargetPosition: N
      TargetArrowHead:
        Type: Open
    - Source: User
      SourcePosition: S
      Target: ALB
      TargetPosition: N
      TargetArrowHead:
        Type: Open
```

This comprehensive guide should enable any coding agent to create accurate and professional AWS architecture diagrams using awsdac. 
