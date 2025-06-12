import { createMcpServer, resource } from "@modelcontextprotocol/sdk/server/mcp.js";
import { Gitlab } from "gitlab";

// Setup your MCP server
const app = createMcpServer();

// Configure GitLab API
const GITLAB_TOKEN = process.env.GITLAB_TOKEN;
const GITLAB_HOST = process.env.GITLAB_HOST || "https://gitlab.com";

if (!GITLAB_TOKEN) {
  throw new Error("Set GITLAB_TOKEN in your environment.");
}

const gitlab = new Gitlab({ token: GITLAB_TOKEN, host: GITLAB_HOST });

/**
 * Recursively fetch all nested subgroups under a group.
 */
async function fetchAllNestedGroups(groupId: string | number, depth = 0, maxDepth = 10): Promise<any[]> {
  if (depth > maxDepth) return [];
  let subgroups: any[] = [];
  try {
    const direct = await gitlab.Groups.subgroups(groupId);
    for (const group of direct) {
      subgroups.push({ id: group.id, name: group.name, full_path: group.full_path });
      const nested = await fetchAllNestedGroups(group.id, depth + 1, maxDepth);
      subgroups = subgroups.concat(nested);
    }
  } catch (err) {
    // You can add logging or error handling here.
  }
  return subgroups;
}

// Register the MCP resource
app.use(
  resource({
    name: "all-nested-groups",
    path: "/all-nested-groups/:groupId",
    description: "Recursively fetches all subgroups under a GitLab group.",
    params: {
      groupId: { type: "string", description: "GitLab Group ID" }
    },
    // Handler for the resource
    async handler({ params }) {
      const { groupId } = params;
      const nested = await fetchAllNestedGroups(groupId);
      return { groupId, nestedGroups: nested };
    }
  })
);

// Start the MCP server
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`MCP server running on port ${PORT}`);
});
