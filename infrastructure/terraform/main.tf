provider "azurerm" {
  features {}
}

provider "aws" {
  region = var.aws_region
}

resource "azurerm_resource_group" "replication" {
  name     = "rg-${var.project_name}-replication-${var.environment}"
  location = var.location
}

# --- Replication Control Plane (AKS) ---

resource "azurerm_kubernetes_cluster" "replication_k8s" {
  name                = "aks-sync-iq-${var.environment}"
  location            = azurerm_resource_group.replication.location
  resource_group_name = azurerm_resource_group.replication.name
  dns_prefix          = "replication-k8s"

  default_node_pool {
    name       = "default"
    node_count = 3
    vm_size    = "Standard_D2s_v3"
  }

  identity {
    type = "SystemAssigned"
  }
}

# --- Replication Metadata Store (Postgres) ---

resource "azurerm_postgresql_flexible_server" "metadata" {
  name                   = "psql-sync-metadata-${var.environment}"
  resource_group_name    = azurerm_resource_group.replication.name
  location               = azurerm_resource_group.replication.location
  version                = "13"
  administrator_login    = "syncadmin"
  administrator_password = var.db_password
  storage_mb             = 32768
  sku_name               = "GP_Standard_D2ds_v4"
}

# --- Event Stream Hub (Kafka / Event Hubs) ---

resource "azurerm_eventhub_namespace" "sync_hub" {
  name                = "eh-sync-hub-${var.environment}"
  location            = azurerm_resource_group.replication.location
  resource_group_name = azurerm_resource_group.replication.name
  sku                 = "Standard"
  capacity            = 1
}

# --- Multi-Cloud Transit (AWS S3 Replication Target) ---

resource "aws_s3_bucket" "sync_landing" {
  bucket = "data-sync-landing-${var.environment}"
}
